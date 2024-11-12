from edc_action_item.model_mixins import ActionModelMixin

from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from django_crypto_fields.fields import IdentityField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import age, get_utcnow
from edc_consent.field_mixins import (
    CitizenFieldsMixin, VulnerabilityFieldsMixin, ReviewFieldsMixin,
    VerificationFieldsMixin)
from edc_consent.field_mixins import IdentityFieldsMixin, PersonalFieldsMixin
from edc_consent.validators import eligible_if_yes
from edc_constants.choices import YES_NO, GENDER, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from ..action_items import CHILDASSENT_ACTION
from ..choices import IDENTITY_TYPE
from ..helper_classes.utils import child_utils
from .eligibility import AssentEligibility
from .model_mixins import SearchSlugModelMixin


class ChildAssentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(
            subject_identifier=subject_identifier)


class ChildAssent(SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin,
                  IdentityFieldsMixin, PersonalFieldsMixin, ReviewFieldsMixin,
                  VulnerabilityFieldsMixin, CitizenFieldsMixin, SearchSlugModelMixin,
                  ActionModelMixin, VerificationFieldsMixin, BaseUuidModel):

    tracking_identifier_prefix = 'CA'

    action_name = CHILDASSENT_ACTION

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True)

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
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

    identity = IdentityField(
        verbose_name='Identity number',
        null=True,
        blank=True)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE,
        null=True,
        blank=True)

    confirm_identity = IdentityField(
        help_text='Retype the identity number',
        null=True,
        blank=True)

    remain_in_study = models.CharField(
        max_length=3,
        verbose_name=('Are you willing to continue the study when you reach 18'
                      ' years of age?'),
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
        default=NOT_APPLICABLE,
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
        max_length=3)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    objects = ChildAssentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier}'

    def natural_key(self):
        return self.subject_identifier

    @property
    def consent_version_cls(self):
        return django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(
            'flourish_caregiver.subjectconsent')

    @property
    def latest_consent_version(self):
        version = None

        try:
            consent_version_obj = self.consent_version_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            version = '1'
        else:
            version = getattr(
                consent_version_obj, 'child_version') or consent_version_obj.version
        return version

    @property
    def child_age(self):
        child_age = age(self.dob, get_utcnow())
        return child_age.years

    def save(self, *args, **kwargs):
        eligibility_criteria = AssentEligibility(
            self.remain_in_study, self.hiv_testing, self.preg_testing, self.child_age)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        if not self.version:
            self.version = self.latest_consent_version

        if self.is_eligible and not self.subject_identifier:
                self.subject_identifier = self.update_subject_identifier

        super().save(*args, **kwargs)

    @property
    def update_subject_identifier(self):
        subject_consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        try:
            consent = subject_consent_cls.objects.get(
                screening_identifier=self.screening_identifier,
                version=self.version)
        except subject_consent_cls.DoesNotExist:
            raise ValidationError(
                'Please complete the adult participation consent '
                f'v{self.version} first.')
        else:
            children_count = 1 + child_utils.registered_subject_cls.objects.filter(
                relative_identifier=consent.subject_identifier).exclude(
                    identity=self.identity).count()
            child_identifier_postfix = '-' + str(children_count * 10)
            return consent.subject_identifier + child_identifier_postfix

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Child Assent for Participation'
        verbose_name_plural = 'Child Assent for Participation'
        unique_together = (('subject_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'last_name', 'identity', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
