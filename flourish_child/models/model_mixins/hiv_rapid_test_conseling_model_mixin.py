from django.db import models
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO
from edc_protocol.validators import date_not_before_study_start

from flourish_child.choices import POS_NEG_IND


class HivRapidTestCounselingModelMixin(models.Model):
    """ A model completed by the user on the caregiver's hiv rapid testing and
            counseling.
        """

    rapid_test_done = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO,
        max_length=3)

    result_date = models.DateField(
        validators=[
            date_not_before_study_start,
            date_not_future, ],
        verbose_name="Date of rapid test",
        blank=True,
        null=True)

    result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG_IND,
        max_length=15,
        blank=True,
        null=True)

    comments = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        null=True)

    class Meta:
        abstract = True
