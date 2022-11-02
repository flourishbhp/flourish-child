from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import YES_NO_COVID_FORM,YES_NO_DN_PNTA, POS_NEG_PENDING_UNKNOWN


class Covid19Adol(ChildCrfModelMixin):
    test_for_covid = models.CharField(
        verbose_name='Have you been tested for COVID-19?',
        max_length=35,
        choices=YES_NO_COVID_FORM,
    )

    receive_test_result = models.CharField(
        verbose_name='Did you receive the result of the test?',
        choices=YES_NO_DN_PNTA,
        max_length=30,
        null=True,
        blank=True,
        help_text='If no/ I do not know /prefer not to answer, end of CRF'
    )

    result_of_test = models.CharField(
        verbose_name='What was the result of the test?',
        choices=POS_NEG_PENDING_UNKNOWN,
        max_length=30,
        null=True,
        blank=True
    )

    class Meta:
        app_label = 'flourish_child'

