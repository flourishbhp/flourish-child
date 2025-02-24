from django.db import models
from edc_base import get_utcnow
from edc_base.model_validators import date_not_future
from edc_constants.choices import POS_NEG, YES_NO, YES_NO_NA,YES_NO_UNKNOWN_NA,YES_NO_UNKNOWN
from edc_constants.constants import NOT_APPLICABLE
from edc_protocol.validators import date_not_before_study_start


class PregTestModelMixin(models.Model):
    experienced_pregnancy = models.CharField(
        verbose_name=('Have you experienced pregnancy since the last contact with '
                      'FLOURISH staff?'),
        max_length=25,
        choices=YES_NO_UNKNOWN_NA,
        default=NOT_APPLICABLE)

    test_done = models.CharField(
        verbose_name='Was a pregnancy test performed?',
        max_length=17,
        choices=YES_NO_NA)

    menarche = models.CharField(
        verbose_name='Has the child reached menarche since the last scheduled visit?',
        max_length=25,
        choices=YES_NO_UNKNOWN)

    menarche_start_dt = models.DateField(
        verbose_name='Start date of menarche',
        validators=[date_not_future],
        null=True,
        blank=True)

    menarche_start_est = models.CharField(
        verbose_name='Is the start date of menarche estimated?',
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    test_date = models.DateField(
        verbose_name='Date of pregnancy test',
        default=get_utcnow,
        validators=[date_not_future, date_not_before_study_start],
        blank=True,
        null=True, )

    preg_test_result = models.CharField(
        verbose_name='What is the result of the pregnancy test?',
        max_length=10,
        choices=POS_NEG,
        blank=True,
        null=True, )

    last_menstrual_period = models.DateField(
        verbose_name='Date of Last Menstrual Period (DD/MMM/YYYY)',
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    is_lmp_date_estimated = models.CharField(
        verbose_name='Is the Last Menstrual Period date estimated?',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,
    )

    comments = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
