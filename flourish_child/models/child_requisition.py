from django.apps import apps as django_apps
from django.conf import settings
from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_lab.choices import PRIORITY
from edc_lab.models import RequisitionIdentifierMixin
from edc_lab.models import RequisitionModelMixin, RequisitionStatusMixin
from edc_metadata.model_mixins.updates import UpdatesRequisitionMetadataModelMixin
from edc_reference.model_mixins import RequisitionReferenceModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_visit_schedule.model_mixins import SubjectScheduleCrfModelMixin
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin
from edc_visit_tracking.model_mixins import PreviousVisitModelMixin

from ..choices import STUDY_SITES, REASON_NOT_DRAWN
from .child_visit import ChildVisit
from .model_mixins import SearchSlugModelMixin, ConsentVersionModelModelMixin


# from edc_senaite_interface.model_mixins import SenaiteRequisitionModelMixin
class ChildRequisitionManager(VisitTrackingCrfModelManager, SearchSlugManager):
    pass


class ChildRequisition(
    NonUniqueSubjectIdentifierFieldMixin, ConsentVersionModelModelMixin,
    RequisitionModelMixin, RequisitionStatusMixin,
    RequisitionIdentifierMixin, VisitTrackingCrfModelMixin,
    SubjectScheduleCrfModelMixin, RequiresConsentFieldsModelMixin,
    PreviousVisitModelMixin, RequisitionReferenceModelMixin,
    UpdatesRequisitionMetadataModelMixin, SearchSlugModelMixin,
    # SenaiteRequisitionModelMixin,
    BaseUuidModel):

    lab_profile_name = 'flourish_child_lab_profile'

    child_visit = models.ForeignKey(ChildVisit, on_delete=PROTECT)

    study_site = models.CharField(
        verbose_name='Study site',
        max_length=25,
        choices=STUDY_SITES,
        default=settings.DEFAULT_STUDY_SITE)

    estimated_volume = models.DecimalField(
        verbose_name='Estimated volume in mL',
        max_digits=7,
        decimal_places=2,
        help_text=(
            'If applicable, estimated volume of sample for this test/order. '
            'This is the total volume if number of "tubes" above is greater than 1'),
        blank=True,
        null=True)

    item_count = models.IntegerField(
        verbose_name='Total number of items',
        help_text=(
            'Number of tubes, samples, cards, etc being sent for this test/order only. '
            'Determines number of labels to print'),
        blank=True,
        null=True)

    priority = models.CharField(
        verbose_name='Priority',
        max_length=25,
        choices=PRIORITY,
        default='normal',)

    reason_not_drawn = models.CharField(
        verbose_name='If not drawn, please explain',
        max_length=25,
        default=NOT_APPLICABLE,
        choices=REASON_NOT_DRAWN)

    comments = models.TextField(
        max_length=350,
        null=True,
        blank=True)

    objects = ChildRequisitionManager()

    history = HistoricalRecords()

    def __str__(self):
        return (
            f'{self.requisition_identifier} '
            f'{self.panel_object.verbose_name}')

    def save(self, *args, **kwargs):
        if not self.id:
            edc_protocol_app_config = django_apps.get_app_config(
                'edc_protocol')
            self.protocol_number = edc_protocol_app_config.protocol_number
        self.report_datetime = self.requisition_datetime
        self.subject_identifier = self.child_visit.subject_identifier
        self.consent_model = 'flourish_caregiver.caregiverchildconsent'
        super().save(*args, **kwargs)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend([
            'requisition_identifier',
            'human_readable_identifier', 'identifier_prefix'])
        return fields

    @property
    def senaite_priority(self):
        """Overrides senaite interface priority mapping.
        """
        priorities = {'normal': '3', 'urgent': '1'}
        return priorities.get(self.priority)

    @property
    def dob(self):
        """Overrides senaite interface dob.
        """
        return self.consent_obj.child_dob

    @property
    def initials(self):
        """Overrides senaite interface participant initials.
        """
        first_name = self.consent_obj.first_name
        last_name = self.consent_obj.last_name
        initials = ''
        if first_name and last_name:
            if (len(first_name.split(' ')) > 1):
                first = first_name.split(' ')[0]
                middle = first_name.split(' ')[1]
                initials = f'{first[:1]}{middle[:1]}{last_name[:1]}'
            else:
                initials = f'{first_name[:1]}{last_name[:1]}'
        return initials

    class Meta:
        app_label = 'flourish_child'
        unique_together = ('panel', 'child_visit')
