from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager

from ..helper_classes.utils import child_utils


class ChildOffSchedule(OffScheduleModelMixin, BaseUuidModel):

    schedule_name = models.CharField(
        max_length=25,
        blank=True,
        null=True)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    objects = SubjectIdentifierManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    def take_off_schedule(self):
        pass

    def get_consent_version(self):
        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

        screening_identifiers = []
        preg_screening_obj = child_utils.preg_screening_model_obj(
            subject_identifier=self.subject_identifier)
        screening_identifiers.append(
            getattr(preg_screening_obj, 'screening_identifier', None))
        prior_screening_obj = child_utils.prior_screening_model_obj(
            subject_identifier=self.subject_identifier)
        screening_identifiers.append(
            getattr(prior_screening_obj, 'screening_identifier', None))

        if not all(idx is None for idx in screening_identifiers):
            try:
                consent_version_obj = consent_version_cls.objects.get(
                    screening_identifier__in=screening_identifiers)
            except consent_version_cls.DoesNotExist:
                raise ValidationError(
                    'Missing Consent Version form. Please complete '
                    'it before proceeding.')

            return consent_version_obj.child_version or consent_version_obj.version

    def save(self, *args, **kwargs):
        self.consent_version = self.get_consent_version()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
