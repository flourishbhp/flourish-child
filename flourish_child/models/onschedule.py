from django import forms
from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager
from edc_visit_schedule.model_mixins import OnScheduleModelMixin as BaseOnScheduleModelMixin


class OnScheduleModelMixin(BaseOnScheduleModelMixin, BaseUuidModel):
    """A model used by the system. Auto-completed by enrollment model.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    schedule_name = models.CharField(max_length=25,
                                     blank=True,
                                     null=True)

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def put_on_schedule(self):
        pass

    def save(self, *args, **kwargs):
        self.consent_version = self.latest_consent_obj_version
        super().save(*args, **kwargs)

    @property
    def consent_version_cls(self):
        return django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(
            'flourish_caregiver.subjectconsent')

    @property
    def latest_consent_obj_version(self):
        child_consent_cls = django_apps.get_model(
            'flourish_child.childdummysubjectconsent')

        subject_consents = child_consent_cls.objects.filter(
             subject_identifier=self.subject_identifier,)
        if subject_consents:
            latest_consent = subject_consents.latest('consent_datetime')
            return latest_consent.version
        else:
            raise forms.ValidationError(
                'Missing dummy consent obj, cannot proceed.')

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
        abstract = True


class OnScheduleChildCohortAEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortAFU(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortAFUQuart(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortABirth(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortAQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBFU(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBFUQuart(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCFU(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCFUQuart(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCPool(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortASec(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortASecQuart(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBSec(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBSecQuart(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCSecQuart(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCSec(OnScheduleModelMixin):
    pass


class OnScheduleChildTbAdolSchedule(OnScheduleModelMixin):
    pass


class OnScheduleTbAdolFollowupSchedule(OnScheduleModelMixin):
    pass
