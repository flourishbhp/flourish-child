from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_constants.choices import YES_NO

from .list_models import TbDiagnostics
from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import (EVAL_LOCATION, CLINIC_NON_VISIT_REASONS,
                       POS_NEG_PENDING_NOT_RECEIVED, XRAY_RESULTS)


class TbAdolReferralOutcomes(ChildCrfModelMixin):

    tb_eval = models.CharField(
        verbose_name='Did participant go to a referral clinic for TB evaluation?',
        max_length=3,
        choices=YES_NO)

    reason_not_going = models.CharField(
        verbose_name='Reason for not going to a referral clinic',
        choices=CLINIC_NON_VISIT_REASONS,
        max_length=50,
        null=True,
        blank=True
    )

    reason_not_going_other = OtherCharField()

    tb_eval_comments = models.TextField(
        verbose_name='Comments',
        max_length=200,
        null=True,
        blank=True)

    tb_eval_location = models.CharField(
        verbose_name='If yes, which clinic did you go to?',
        max_length=50,
        choices=EVAL_LOCATION,
        null=True,
        blank=True
    )

    tb_eval_location_other = OtherCharField()

    tb_diagnostic_perf = models.CharField(
        verbose_name='Were TB diagnostic studies performed at the clinic visit?',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True)

    tb_diagnostics = models.ManyToManyField(
        TbDiagnostics,
        verbose_name='What TB diagnostic studies were performed? ',
        blank=True)

    tb_diagnostics_other = OtherCharField()

    sputum_sample = models.CharField(
        verbose_name='Sputum Sample',
        choices=POS_NEG_PENDING_NOT_RECEIVED,
        max_length=13,
        null=True,
        blank=True
    )

    chest_xray = models.CharField(
        verbose_name='Chest x-ray',
        choices=XRAY_RESULTS,
        max_length=13,
        null=True,
        blank=True
    )

    gene_xpert = models.CharField(
        verbose_name='Gene Xpert',
        choices=POS_NEG_PENDING_NOT_RECEIVED,
        max_length=13,
        null=True,
        blank=True
    )
    tst_or_mentoux = models.CharField(
        verbose_name='TST/Mantoux',
        choices=POS_NEG_PENDING_NOT_RECEIVED,
        max_length=13,
        null=True,
        blank=True
    )

    covid_19 = models.CharField(
        verbose_name='COVID-19',
        choices=XRAY_RESULTS,
        max_length=13,
        null=True,
        blank=True
    )

    tb_treat_start = models.CharField(
        verbose_name='Was TB treatment started?',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True)

    tb_prev_therapy_start = models.CharField(
        verbose_name='Was TB preventative therapy started?',
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True)

    tb_comments = models.TextField(
        verbose_name='Comments',
        max_length=250,
        null=True,
        blank=True)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB Referral Outcomes'
        verbose_name_plural = "TB Referral Outcomes"
