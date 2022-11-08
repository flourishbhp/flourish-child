from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager
from edc_visit_schedule.model_mixins import OffScheduleModelMixin


# from .model_mixins import ConsentVersionModelModelMixin
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
        preg_subject_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpregwomen')
        prior_subject_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpriorbhpparticipants')

        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

        subject_screening_obj = None

        try:
            subject_screening_obj = preg_subject_screening_cls.objects.get(
                subject_identifier=self.subject_identifier[:-3])
        except preg_subject_screening_cls.DoesNotExist:

            try:
                subject_screening_obj = prior_subject_screening_cls.objects.get(
                    subject_identifier=self.subject_identifier[:-3])
            except prior_subject_screening_cls.DoesNotExist:
                raise ValidationError(
                    'Missing Subject Screening form. Please complete '
                    'it before proceeding.')

        if subject_screening_obj:
            try:
                consent_version_obj = consent_version_cls.objects.get(
                    screening_identifier=subject_screening_obj.screening_identifier)
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
