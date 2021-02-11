from django.db import models

from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_validators import datetime_not_future
from edc_consent.field_mixins import (
    CitizenFieldsMixin, VulnerabilityFieldsMixin, ReviewFieldsMixin)
from edc_consent.field_mixins import IdentityFieldsMixin, PersonalFieldsMixin
from edc_consent.validators import eligible_if_yes
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from ..choices import IDENTITY_TYPE
from .model_mixins import SearchSlugModelMixin


class ChildAssentManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(
            subject_identifier=subject_identifier)


class ChildAssent(SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin,
                  IdentityFieldsMixin, PersonalFieldsMixin, ReviewFieldsMixin,
                  VulnerabilityFieldsMixin, CitizenFieldsMixin, SearchSlugModelMixin,
                  BaseUuidModel):

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50)

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    remain_in_study = models.CharField(
        max_length=3,
        verbose_name=('Are you willing to continue the study when you reach 18 '
                      'years of age?'),
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text='If no, participant is not eligible.')

    hiv_testing = models.CharField(
        max_length=3,
        verbose_name=('Are you willing to be tested for HIV ?'),
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text='If no, participant is not eligible.')

    preg_testing = models.CharField(
        max_length=3,
        verbose_name='Are you willing to undergo pregnancy testing? ',
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        blank=True,
        null=True,
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

    objects = ChildAssentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier}'

    def natural_key(self):
        return self.subject_identifier

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Child Assent for Participation'
        verbose_name_plural = 'Child Assent for Participation'
        unique_together = (('subject_identifier', 'screening_identifier'),
                           ('first_name', 'dob', 'initials'))
