from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from ..choices import (NO_ART_REASON, ART_PROPH_STATUS, REASON_MODIFIED,
                       CHILD_ARV_PROPH)
from .child_crf_model_mixin import ChildCrfModelMixin


class InfantArvProphylaxis(ChildCrfModelMixin):
    """  """

    took_art_proph = models.CharField(
        max_length=3,
        choices=YES_NO,
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
        verbose_name=('Approximately how many days did the infant '
                      'receive prophylaxis'),
        validators=[MinValueValidator(29), MaxValueValidator(90)],
        null=True,
        blank=True,
        help_text='(range 29 - 90)')

    reason_incomplete = models.CharField(
        verbose_name=('Reason participant did not finish within '
                      'stipulated prophylaxis time'),
        max_length=100,
        null=True,
        blank=True)

    arvs_modified = models.CharField(
        verbose_name=('Was there any modification occurred since '
                      'the baby was started on ARV prophylaxis?'),
        choices=YES_NO,
        max_length=3,
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
        choices=YES_NO_NA,
        max_length=3)

    missed_dose_count = models.PositiveIntegerField(
        verbose_name='How many doses missed?', )
    
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

    arv_start_date = models.DateField(verbose_name='Start date')

    arv_stop_date = models.DateField(verbose_name='Stop date')

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'ARVs Received Dates'
        verbose_name_plural = 'ARVs Received Dates'
        unique_together = ('infant_arv_proph', 'arv_name')
