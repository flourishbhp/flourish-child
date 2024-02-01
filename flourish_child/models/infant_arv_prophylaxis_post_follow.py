from django.core.exceptions import ValidationError
from django.db import models

from flourish_child.choices import YES_NO_DN_RECALL
from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin
from flourish_child.models.list_models import ARTMedicationReasons, ARTProphStatus, \
    ChildArvProph, ChildARVsProphmodReason


def validate_range(value):
    if value < 29 or value > 90:
        raise ValidationError('Value should be between 29 and 90', code='invalid',
                              params={'value': value}, )


class InfantArvProphylaxisPostFollow(ChildCrfModelMixin):
    """Infant ARV Prophylaxis Post Follow-up"""

    last_visit = models.CharField(
        verbose_name='Did the baby take prophylactic antiretroviral medication for '
                     'any period since the last attended scheduled visit? ',
        choices=YES_NO_DN_RECALL,
        max_length=50,
    )

    reason_no_art = models.ManyToManyField(
        ARTMedicationReasons,
        verbose_name='What was the reason the baby did not take antiretroviral '
                     'medication?',
        null=True,
        blank=True,
    )

    reason_no_art_other = models.TextField(
        verbose_name='Other reason',
        null=True,
        blank=True,
    )

    arv_status = models.ManyToManyField(
        ARTProphStatus,
        verbose_name='What is the status of participant\'s ARV prophylaxis at this '
                     'visit?',
        max_length=50,
        null=True,
        blank=True,
    )

    days_completed = models.PositiveIntegerField(
        verbose_name='Approximately how many days did the infant receive prophylaxis',
        default=0,
        null=True,
        blank=True,
        validators=[validate_range],
    )

    incomplete_reason = models.TextField(
        verbose_name='Reason participant did not finish within stipulated prophylaxis '
                     'time',
        null=True,
        blank=True,
    )

    arv_taken = models.ManyToManyField(
        ChildArvProph,
        verbose_name='What ARV  did the baby take? ',
        max_length=50,
    )

    nvp_start_date = models.DateField(
        verbose_name='Date NVP started',
        null=True,
        blank=True,
    )

    nvp_end_date = models.DateField(
        verbose_name='Date NVP ended',
        null=True,
        blank=True,
    )

    azt_start_date = models.DateField(
        verbose_name='Date AZT started',
        null=True,
        blank=True,
    )

    azt_end_date = models.DateField(
        verbose_name='Date AZT ended',
        null=True,
        blank=True,
    )

    start_date_3tc = models.DateField(
        verbose_name='Date 3TC started',
        null=True,
        blank=True,
    )

    end_date_3tc = models.DateField(
        verbose_name='Date 3TC ended',
        null=True,
        blank=True,
    )

    ftc_start_date = models.DateField(
        verbose_name='Date FTC started',
        null=True,
        blank=True,
    )

    ftc_end_date = models.DateField(
        verbose_name='Date FTC ended',
        null=True,
        blank=True,
    )

    alu_start_date = models.DateField(
        verbose_name='Date ALU started',
        null=True,
        blank=True,
    )

    alu_end_date = models.DateField(
        verbose_name='Date ALU ended',
        null=True,
        blank=True,
    )

    trv_start_date = models.DateField(
        verbose_name='Date TRV started',
        null=True,
        blank=True,
    )

    trv_end_date = models.DateField(
        verbose_name='Date TRV ended',
        null=True,
        blank=True,
    )

    tdf_start_date = models.DateField(
        verbose_name='Date TDF started',
        null=True,
        blank=True,
    )

    tdf_end_date = models.DateField(
        verbose_name='Date TDF ended',
        null=True,
        blank=True,
    )

    abc_start_date = models.DateField(
        verbose_name='Date ABC started',
        null=True,
        blank=True,
    )

    abc_end_date = models.DateField(
        verbose_name='Date ABC ended',
        null=True,
        blank=True,
    )

    ral_start_date = models.DateField(
        verbose_name='Date RAL started',
        null=True,
        blank=True,
    )

    ral_end_date = models.DateField(
        verbose_name='Date RAL ended',
        null=True,
        blank=True,
    )

    mod_starting_arv = models.CharField(
        verbose_name='Was there any Modification occurred since the baby was started on '
                     'ARV prophylaxis?',
        choices=YES_NO_DN_RECALL,
        max_length=50,
    )

    mod_date = models.DateField(
        verbose_name='Date modification occurred',
        null=True,
        blank=True,
    )

    mod_reason = models.ManyToManyField(
        ChildARVsProphmodReason,
        verbose_name='If yes, what was the reason?',
        null=True,
        blank=True,
    )

    mod_reason_other = models.CharField(
        verbose_name='Other reason',
        max_length=50,
        null=True,
        blank=True,
    )

    mod_reason_side_effects = models.TextField(
        verbose_name='If side effects, specify',
        null=True,
        blank=True,
    )

    missed_dose = models.CharField(
        verbose_name='Has the baby missed any dose since last scheduled visit?',
        choices=YES_NO_DN_RECALL,
        max_length=50,
        null=True,
        blank=True,
    )

    missed_dose_count = models.PositiveIntegerField(
        verbose_name='How many doses missed?',
        default=0,
        null=True,
        blank=True,
    )

    reason_missed = models.TextField(
        verbose_name='Reason for missing doses',
        null=True,
        blank=True,
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant ARV Prophylaxis Post Follow-up'
        verbose_name_plural = 'Infant ARV Prophylaxis Post Follow-up'
