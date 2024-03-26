from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from flourish_child.choices import DELIVERY_LOCATION, POS_NEG_PENDING_UNKNOWN


class HIVTestingAndResultingMixin(models.Model):

    child_test_date_estimated = models.CharField(
        verbose_name='Was this date estimated?',
        choices=YES_NO,
        max_length=20,
    )

    test_location = models.CharField(
        verbose_name='Where was the test done?',
        choices=DELIVERY_LOCATION,
        max_length=100,
    )

    test_location_other = OtherCharField()

    results_received = models.CharField(
        verbose_name='Have you received the results of this test?',
        choices=YES_NO,
        max_length=20,
        help_text='request participant to seek HIV Results from clinic'
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

    additional_comments = models.TextField(
        verbose_name='Additional comments:',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
