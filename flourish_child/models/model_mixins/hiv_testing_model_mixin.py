from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_DONT_KNOW

from flourish_child.choices import POS_NEG_PENDING_UNKNOWN, PREFERRED_CLINIC
from flourish_child.models.list_models import ChildHIVNotTestedReason, ChildHIVTestVisits


class HivTestingModelMixin(models.Model):
    child_tested_for_hiv = models.CharField(
        verbose_name='Has your child been tested for HIV since the last study visit?',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
        help_text='Do not include the HIV test completed at the FLOURISH visit'
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
        verbose_name='Do you recall the date you received this test result, or even the '
                     'month?',
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

    test_visit = models.ManyToManyField(
        ChildHIVTestVisits,
        verbose_name='Were any of the following HIV tests been performed since the last '
                     'visit ',
        max_length=100,
        blank=True
    )

    test_visit_other = OtherCharField()

    reason_child_not_tested = models.ManyToManyField(
        ChildHIVNotTestedReason,
        verbose_name='Was there a reason your child was not tested for HIV? ',
        max_length=100,
        blank=True
    )

    pref_location = models.CharField(
        verbose_name='Do you prefer to go to the local clinic or to come to the FLOURISH'
                     ' CLINIC for testing your child?',
        choices=PREFERRED_CLINIC,
        max_length=100,
        default='',
        help_text='Not application would be selected if the child is not due for testing'
    )

    pref_location_other = OtherCharField()

    reason_child_not_tested_other = models.TextField(
        verbose_name='If “Other”, please specify:',
        null=True,
        blank=True
    )

    preferred_clinic_for_testing = models.CharField(
        verbose_name='Do you prefer to go to the local clinic or to come '
                     'to the FLOURISH CLINIC for '
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
    )

    class Meta:
        abstract = True
