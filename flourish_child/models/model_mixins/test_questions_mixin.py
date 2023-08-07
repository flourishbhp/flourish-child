from django.db import models
from edc_constants.choices import YES_NO

from flourish_child.choices import CBCL_IMPACT, CBCL_INTEREST, CBCL_INVALID_REASON, \
    CBCL_UNDERSTANDING


class TestQuestionMixin(models.Model):
    caregiver_interest = models.CharField(
        verbose_name='How interested was the caregiver in completing the test?',
        choices=CBCL_INTEREST,
        max_length=30,
        blank=True,
        null=True)

    caregiver_understanding = models.CharField(
        verbose_name='For this test, how well did the caregiver understand the '
                     'questions being asked?',
        choices=CBCL_UNDERSTANDING,
        max_length=30,
        blank=True,
        null=True)

    valid = models.CharField(
        verbose_name='In your opinion, are the results of the test valid?',
        choices=YES_NO,
        max_length=10,
        blank=True,
        null=True)

    invalid_reason = models.CharField(
        verbose_name='If the test was NOT VALID, specify the reason why it was not '
                     'valid:',
        choices=CBCL_INVALID_REASON,
        max_length=100,
        blank=True,
        null=True)

    impact_on_responses = models.CharField(
        verbose_name='Did any of the following impact responses to the test questions:',
        choices=CBCL_IMPACT,
        max_length=50,
        blank=True,
        null=True)

    overall_comments = models.TextField(
        verbose_name='Overall comments for the test:',
        max_length=1000,
        blank=True,
        null=True)

    class Meta:
        abstract = True
