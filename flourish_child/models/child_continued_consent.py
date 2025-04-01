from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future, eligible_if_yes
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_consent.field_mixins import (CitizenFieldsMixin, IdentityFieldsMixin,
                                      PersonalFieldsMixin, ReviewFieldsMixin,
                                      VulnerabilityFieldsMixin)
from edc_constants.choices import GENDER, YES_NO, YES_NO_NA
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from .eligibility import ContinuedConsentEligibility
from .model_mixins import SearchSlugModelMixin
from ..choices import IDENTITY_TYPE


class ChildContinuedConsentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(
            subject_identifier=subject_identifier)


class ChildContinuedConsent(SiteModelMixin, IdentityFieldsMixin, PersonalFieldsMixin,
                            ReviewFieldsMixin, VulnerabilityFieldsMixin,
                            CitizenFieldsMixin, SearchSlugModelMixin, BaseUuidModel):
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
        max_length=1, )

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
        verbose_name='Are you willing to be tested for HIV ?',
        choices=YES_NO,
        help_text='If no, participant is not eligible.')

    preg_testing = models.CharField(
        max_length=3,
        verbose_name='Are you willing to undergo pregnancy testing? ',
        choices=YES_NO_NA,
        help_text='If ‘No’ ineligible for study participation')

    specimen_consent = models.CharField(
        max_length=3,
        verbose_name='Do you give us permission to use your blood samples for future '
                     'studies?',
        choices=YES_NO)

    along_side_caregiver = models.CharField(
        verbose_name='Do you feel comfortable with continuing on the FLOURISH study '
                     'alongside your caregiver?',
        max_length=3,
        choices=YES_NO,
    )

    include_contact_details = models.CharField(
        verbose_name='Will your contact information, including phone numbers and '
                     'physical address, remain the same',
        max_length=3,
        choices=YES_NO,
    )

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
    def child_consent_version_cls(self):
        return django_apps.get_model(
            'flourish_child.childconsentversion')

    @property
    def latest_child_consent_version(self):
        version = None
        try:
            consent_version_obj = self.child_consent_version_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except self.child_consent_version_cls.DoesNotExist:
            version = None
        else:
            version = getattr(consent_version_obj, 'version', None)
        return version

    def save(self, *args, **kwargs):
        eligibility_criteria = ContinuedConsentEligibility(
            self.remain_in_study, self.hiv_testing, self.preg_testing)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        if not self.version:
            self.version = self.latest_child_consent_version
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Child Continued Consent'
        unique_together = (('subject_identifier', 'version'),)
