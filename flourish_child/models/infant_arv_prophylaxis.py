from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future, dob_not_today
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import (ART_PROPH_STATUS, CHILD_ARV_PROPH, NO_ART_REASON, REASON_MODIFIED,
                       YES_NO_DN_RECALL)


class InfantArvProphylaxis(ChildCrfModelMixin):
    """  """

    took_art_proph = models.CharField(
        max_length=20,
        choices=YES_NO_DN_RECALL,
        verbose_name=('Did the baby take prophylactic antiretroviral '
                      'medication for any period since the last '
                      'attended scheduled visit?'))

    reason_no_art = models.CharField(
        verbose_name=('What was the reason the baby did not take '
                      'antiretroviral medication?'),
        choices=NO_ART_REASON,
        max_length=22,
        null=True,
        blank=True)

    reason_no_art_other = OtherCharField()

    art_status = models.CharField(
        verbose_name=('What is the status of participant\'s ARV '
                      'prophylaxis at this visit?'),
        choices=ART_PROPH_STATUS,
        max_length=22,
        null=True,
        blank=True)

    days_art_received = models.IntegerField(
        verbose_name=('If completed PMTCT intervention with prophylaxis '
                      'greater than 28days. Approximately how many days '
                      'did the infant receive prophylaxis'),
        validators=[MinValueValidator(29), MaxValueValidator(90)],
        null=True,
        blank=True,
        help_text='(range 29 - 90)')

    reason_incomplete = models.TextField(
        verbose_name=('Reason participant did not finish within '
                      'stipulated prophylaxis time'),
        null=True,
        blank=True)

    arvs_modified = models.CharField(
        verbose_name=('Was there any modification occurred since '
                      'the baby was started on ARV prophylaxis?'),
        choices=YES_NO_DN_RECALL,
        max_length=20,
        null=True,
        blank=True)

    date_arvs_modified = models.DateField(
        verbose_name='Date modification occured',
        null=True,
        blank=True)

    reason_modified = models.CharField(
        verbose_name='If yes, what was the reason?',
        choices=REASON_MODIFIED,
        max_length=20,
        null=True,
        blank=True)

    specify_effects = models.CharField(
        verbose_name='If side effects, specify',
        max_length=100,
        null=True,
        blank=True)

    reason_modified_othr = OtherCharField()

    missed_dose = models.CharField(
        verbose_name='Has the baby missed any dose since last scheduled visit?',
        choices=YES_NO_DN_RECALL,
        max_length=20,
        blank=True,
        null=True)

    missed_dose_count = models.PositiveIntegerField(
        verbose_name='How many doses missed?',
        null=True,
        blank=True,
        default=0)

    reason_missed = models.TextField(
        verbose_name='Reason for missing doses',
        null=True,
        blank=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant ARV Prophylaxis'
        verbose_name_plural = 'Infant ARV Prophylaxis'


class ChildArvProphDates(CrfInlineModelMixin, BaseUuidModel):
    infant_arv_proph = models.ForeignKey(
        InfantArvProphylaxis, on_delete=models.PROTECT)

    arv_name = models.CharField(
        'What ARV did the baby take?',
        choices=CHILD_ARV_PROPH,
        max_length=15)

    arv_start_date = models.DateField(
        verbose_name='Start date',
        validators=[date_not_future, dob_not_today]
    )

    arv_stop_date = models.DateField(
        verbose_name='Stop date',
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'ARVs Received Dates'
        verbose_name_plural = 'ARVs Received Dates'
        unique_together = ('infant_arv_proph', 'arv_name')
