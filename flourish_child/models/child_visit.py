from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager as BaseCurrentSiteManager
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_fields.custom_fields import OtherCharField
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.constants import ALIVE
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_visit_tracking.constants import MISSED_VISIT
from edc_visit_tracking.managers import VisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin, CaretakerFieldsMixin
from flourish_caregiver.choices import UNSCHEDULED_REASON
from .child_appointment import Appointment
from ..choices import ALIVE_DEAD_UNKNOWN, VISIT_INFO_SOURCE
from ..choices import VISIT_STUDY_STATUS, VISIT_REASON, INFO_PROVIDER
from ..visit_sequence import VisitSequence


class CurrentSiteManager(VisitModelManager, BaseCurrentSiteManager):
    pass


class ChildVisit(
        VisitModelMixin, CreatesMetadataModelMixin,
        ReferenceModelMixin, RequiresConsentFieldsModelMixin,
        CaretakerFieldsMixin, SiteModelMixin, BaseUuidModel):

    """ A model completed by the user on child visits. """

    visit_sequence_cls = VisitSequence
    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT)

    reason = models.CharField(
        verbose_name='Reason for visit',
        max_length=25,
        choices=VISIT_REASON)

    reason_missed = models.CharField(
        verbose_name=(
            'If \'missed\' above, reason scheduled '
            'scheduled visit was missed'),
        blank=True,
        null=True,
        max_length=250)

    information_provider = models.CharField(
        verbose_name=(
            'Please indicate who provided most of the information for this child\'s visit'),
        max_length=20,
        choices=INFO_PROVIDER)

    information_provider_other = OtherCharField(
        verbose_name='If Other, specify',
        max_length=25,
        blank=True,
        null=True)

    reason_unscheduled = models.CharField(
        verbose_name=(
            'If \'Unscheduled\' above, provide reason for '
            'the unscheduled visit'),
        blank=True,
        choices=UNSCHEDULED_REASON,
        null=True,
        max_length=30)

    reason_unscheduled_other = models.CharField(
        verbose_name="if unscheduled reason is Other, please specify",
        max_length=100,
        blank=True,
        null=True)

    study_status = models.CharField(
        verbose_name="What is the participant's current study status",
        max_length=50,
        choices=VISIT_STUDY_STATUS)

    survival_status = models.CharField(
        max_length=10,
        verbose_name='Participant\'s survival status',
        choices=ALIVE_DEAD_UNKNOWN,
        null=True,
        default=ALIVE)

    info_source = models.CharField(
        verbose_name='Source of information?',
        max_length=25,
        choices=VISIT_INFO_SOURCE)

    on_site = CurrentSiteManager()

    objects = VisitModelManager()

    history = HistoricalRecords()

    @property
    def action_item_reason(self):
        return self.study_status

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def run_metadata_rules(self, visit=None):
        """Runs all the rule groups.

        Initially called by post_save signal.

        Also called by post_save signal after metadata is updated.
        """
        visit = visit or self

        if visit.reason not in [MISSED_VISIT, 'edc_system_glitch']:
            metadata_rule_evaluator = self.metadata_rule_evaluator_cls(
                visit=visit)
            metadata_rule_evaluator.evaluate_rules()

    class Meta(VisitModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Child Visit"
        verbose_name_plural = "Child Visit"
