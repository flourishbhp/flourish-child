from django.apps import apps as django_apps
from django.db import models
from edc_action_item.model_mixins import ActionModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import eligible_if_yes, datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import (IdentityFieldsMixin, PersonalFieldsMixin,
                                      ReviewFieldsMixin, VulnerabilityFieldsMixin,
                                      CitizenFieldsMixin)
from edc_constants.choices import YES_NO, GENDER, YES_NO_NA
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from ..action_items import CHILDCONTINUEDCONSENT_STUDY_ACTION
from ..choices import IDENTITY_TYPE
from .eligibility import ContinuedConsentEligibility
from .model_mixins import SearchSlugModelMixin


class ChildContinuedConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(
            subject_identifier=subject_identifier)


class ChildContinuedConsent(SiteModelMixin, IdentityFieldsMixin, PersonalFieldsMixin,
                            ReviewFieldsMixin, VulnerabilityFieldsMixin,
                            CitizenFieldsMixin, SearchSlugModelMixin,
                            ActionModelMixin, BaseUuidModel):

    tracking_identifier_prefix = 'CC'

    action_name = CHILDCONTINUEDCONSENT_STUDY_ACTION

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    citizen = models.CharField(
        verbose_name='Is the participant a Botswana citizen? ',
        max_length=3,
        validators=[eligible_if_yes, ],
        choices=YES_NO,
        help_text='If ‘No’ ineligible for study participation')

    gender = models.CharField(
        verbose_name='Gender',
        choices=GENDER,
        max_length=1,)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    remain_in_study = models.CharField(
        max_length=3,
        verbose_name=('Are you willing to continue to participate in the FLOURISH'
                      ' study?'),
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    hiv_testing = models.CharField(
        max_length=3,
        verbose_name=('Are you willing to be tested for HIV ?'),
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    preg_testing = models.CharField(
        max_length=3,
        verbose_name='Are you willing to undergo pregnancy testing? ',
        choices=YES_NO_NA,
        help_text='If ‘No’ ineligible for study participation')

    specimen_consent = models.CharField(
        max_length=3,
        verbose_name='Do you give us permission to use your blood samples for future studies?',
        choices=YES_NO)

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future])

    version = models.CharField(
        max_length=1)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    objects = ChildContinuedConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier}, V{self.version}'

    def natural_key(self):
        return self.subject_identifier

    @property
    def consent_version_cls(self):
        return django_apps.get_model('flourish_caregiver.flourishconsentversion')

    @property
    def subject_consent_cls(self):
        return django_apps.get_model('flourish_caregiver.subjectconsent')

    @property
    def latest_consent_version(self):
        subject_identifier = self.subject_identifier.split('-')
        subject_identifier.pop()
        caregiver_subject_identifier = '-'.join(subject_identifier)

        version = None
        try:
            consent = self.subject_consent_cls.objects.filter(
                subject_identifier=caregiver_subject_identifier)
        except self.subject_consent_cls.ObjectDoesNotExist:
            return None
        else:
            latest_consent = consent[0]
            try:
                consent_version_obj = self.consent_version_cls.objects.get(
                    screening_identifier=latest_consent.screening_identifier)
            except self.consent_version_cls.DoesNotExist:
                version = '1'
            else:
                version = consent_version_obj.version
            return version

    def save(self, *args, **kwargs):
        eligibility_criteria = ContinuedConsentEligibility(
            self.remain_in_study, self.hiv_testing, self.preg_testing)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        self.version = self.latest_consent_version
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Child Continued Consent'
        unique_together = (('subject_identifier', 'version'),)
