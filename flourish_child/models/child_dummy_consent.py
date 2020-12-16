from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin

from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.model_mixins import ConsentModelMixin


class ChildDummySubjectConsent(
        ConsentModelMixin, SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin,
        PersonalFieldsMixin, BaseUuidModel):

    """ A dummy child model auto completed by the s. """

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',)

    report_datetime = models.DateTimeField(
        null=True,
        editable=False)

    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,
        help_text='See \'Consent Type\' for consent versions by period.',
        editable=False)

    history = HistoricalRecords()
    
    _cohort_schedule = None

    def __str__(self):
        return f'{self.subject_identifier} V{self.version}'

    def natural_key(self):
        return (self.subject_identifier, self.version)
    
    @property
    def cohort(self):
        #TO-DO: add variable name, e.g 'cohort_a'
        return self._cohort_schedule

    @cohort.setter
    def cohort(self, val):
        self._cohort_schedule = val

    class Meta(ConsentModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child Consent'
        unique_together = (
            ('subject_identifier', 'version'))
