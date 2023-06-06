from django.db import models
from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import POS_NEG_PENDING_UNKNOWN, PREFERRED_CLINIC, NOT_TESTED_REASON
from edc_constants.choices import YES_NO_DONT_KNOW, YES_NO


class InfantHIVTesting(ChildCrfModelMixin):
    child_tested_for_hiv = models.CharField(
        verbose_name='Has your child been tested for HIV since the last study visit?',
        choices=YES_NO_DONT_KNOW,
        max_length=20
    )

    child_test_date = models.DateField(
        verbose_name='What was the date of this test?',
        null=True,
        blank=True
    )

    child_test_date_estimated = models.CharField(
        verbose_name='Was this date estimated?',
        choices=YES_NO,
        max_length=20,
        null=True,
        blank=True
    )

    results_received = models.CharField(
        verbose_name='Have you received the results of this test?',
        choices=YES_NO,
        max_length=20,
        null=True,
        blank=True
    )

    recall_result_date = models.CharField(
        verbose_name='Do you recall the date you received this test result, or even the month?',
        choices=YES_NO,
        max_length=20,
        null=True,
        blank=True
    )

    received_date = models.DateField(
        verbose_name='What date did you receive this test?',
        null=True,
        blank=True
    )

    result_date_estimated = models.CharField(
        verbose_name='Was this date estimated?',
        choices=YES_NO,
        max_length=20,
        null=True,
        blank=True
    )

    hiv_test_result = models.CharField(
        verbose_name='What is the result of the HIV test?',
        choices=POS_NEG_PENDING_UNKNOWN,
        max_length=20,
        null=True,
        blank=True
    )

    reason_child_not_tested = models.CharField(
        verbose_name='Was there a reason your child was not tested for HIV?',
        choices=NOT_TESTED_REASON,
        max_length=100,
        null=True,
        blank=True
    )

    reason_child_not_tested_other = models.TextField(
        verbose_name='If “Other”, please specify:',
        null=True,
        blank=True
    )

    preferred_clinic_for_testing = models.CharField(
        verbose_name='If Q3 is No, Do you prefer to go to the local clinic or to come to the FLOURISH CLINIC for '
                     'testing your child?',
        choices=PREFERRED_CLINIC,
        max_length=100,
        null=True,
        blank=True
    )

    additional_comments = models.TextField(
        verbose_name='Additional comments:',
        null=True,
        blank=True,
        help_text='If answer to Q13 is “I do not wish to have my infant tested at this time” or “Other”, '
                  'please require a comment in the box below: '
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant HIV Testing and Results CRF'
        verbose_name_plural = 'Infant HIV Testing and Results CRFs'
