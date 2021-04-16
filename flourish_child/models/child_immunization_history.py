from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import YES_NO_UNKNOWN, IMMUNIZATIONS, CHILD_AGE_VACCINE_GIVEN
from ..choices import REASONS_VACCINES_MISSED


class ChildImmunizationHistory(ChildCrfModelMixin):
    """ A model completed by the user on the Infant/Child/Adolescent's
        immunization history. """

    vaccines_missed = models.CharField(
        max_length=25,
        choices=YES_NO_UNKNOWN,
        verbose_name='Is the infant/child/adolescent missing any vaccinations?',
        help_text='')

    """Quartely Phone call stem question"""
    rec_add_immunization = models.CharField(
        verbose_name=('Since the last scheduled visit, have you received any '
                      'additional immunizations?'),
        choices=YES_NO_NA,
        max_length=20,
        default=NOT_APPLICABLE)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Immunization History'
        verbose_name_plural = 'Immunization History'


class VaccinesReceived(CrfInlineModelMixin, BaseUuidModel):

    """ALL possible vaccines given to Infant/Child/Adolescent"""

    child_immunization_history = models.ForeignKey(
        ChildImmunizationHistory, on_delete=models.CASCADE)

    received_vaccine_name = models.CharField(
        verbose_name="Received vaccine name",
        choices=IMMUNIZATIONS,
        max_length=100,
        null=True,
        blank=True)

    date_given = models.DateField(
        verbose_name="Date Given",
        validators=[
            date_not_future, ],
        null=True,
        blank=True)

    child_age = models.CharField(
        verbose_name="Infant/Child/Adolescent age when vaccine given",
        choices=CHILD_AGE_VACCINE_GIVEN,
        null=True,
        blank=True,
        max_length=35)

    def natural_key(self):
        return (self.received_vaccine_name,) + self.child_immunization_history.natural_key()

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Received Vaccines'
        verbose_name_plural = 'Received Vaccines'
        unique_together = (
            'received_vaccine_name', 'child_immunization_history', 'child_age')


class VaccinesMissed(CrfInlineModelMixin, BaseUuidModel):

    """All vaccines missed by Infant/Child/Adolescent"""

    parent_model_attr = 'child_immunization_history'

    child_immunization_history = models.ForeignKey(
        ChildImmunizationHistory, on_delete=models.CASCADE)

    missed_vaccine_name = models.CharField(
        verbose_name="Missed vaccine name",
        choices=IMMUNIZATIONS,
        max_length=100,
        null=True,
        blank=True)

    reason_missed = models.CharField(
        verbose_name="Reasons infant/child/adolescent missed vaccines",
        choices=REASONS_VACCINES_MISSED,
        max_length=100,
        null=True,
        blank=True)

    reason_missed_other = OtherCharField()

    def natural_key(self):
        return (self.missed_vaccine_name,) + self.child_immunization_history.natural_key()

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Missed Vaccines'
        verbose_name_plural = 'Missed Vaccines'
        unique_together = (
            'missed_vaccine_name', 'child_immunization_history', 'reason_missed')
