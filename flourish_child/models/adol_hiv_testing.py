
from django.db import models
from django.core.validators import RegexValidator

from ..choices import YES_NO_DN_PNTA, TIMES_TESTED, POS_NEG_IND_IDK
from .child_crf_model_mixin import ChildCrfModelMixin


class HivTestingAdol(ChildCrfModelMixin):
    test_for_hiv = models.CharField(
        verbose_name='Have you tested for HIV since your HIV test at enrollment?',
        choices=YES_NO_DN_PNTA,
        max_length=30
    )

    times_tested = models.CharField(
        verbose_name='How many times have you tested for HIV?',
        choices=TIMES_TESTED,
        max_length=4,
        null=True,
        blank=True,
    )

    last_result = models.CharField(
        verbose_name='What was the result of your last test?',
        choices=POS_NEG_IND_IDK,
        max_length=8,
        null=True,
        blank=True,
    )

    referred_for_treatment = models.CharField(
        verbose_name='Since you were diagnosed with HIV, were you referred to clinic for treatment for HIV?',
        choices=YES_NO_DN_PNTA,
        max_length=10,
        null=True,
        blank=True,
    )

    initiated_treatment = models.CharField(
        verbose_name='Have you initiated treatment for HIV?',
        choices=YES_NO_DN_PNTA,
        max_length=10,
        null=True,
        blank=True,

    )

    date_initiated_treatment = models.CharField(
        verbose_name='Date initiated treatment for HIV',
        help_text='Format MM-YYYY, e.g. 01-2022',
        max_length=10,
        validators=[RegexValidator(regex=r'(0[1-9]|1[0-2])-20[0-9]{2}')],
        null=True,
        blank=True,

    )

    seen_by_healthcare = models.CharField(
        verbose_name=' Since you were diagnosed with HIV, were you seen by a health care worker for evaluation for tuberculosis',
        choices=YES_NO_DN_PNTA,
        max_length=10,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'HIV History'
        verbose_name_plural = 'HIV History'
