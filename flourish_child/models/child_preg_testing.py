from django.db import models

from edc_base.utils import get_utcnow
from edc_base.model_validators import date_not_future
from edc_constants.choices import POS_NEG, YES_NO
from edc_protocol.validators import date_not_before_study_start

from .child_crf_model_mixin import ChildCrfModelMixin


class ChildPregTesting(ChildCrfModelMixin):

    test_done = models.CharField(
        verbose_name='Was a pregnancy test processed?',
        max_length=10,
        choices=YES_NO)

    test_date = models.DateField(
        verbose_name='Date of pregnancy test',
        default=get_utcnow,
        validators=[date_not_future, date_not_before_study_start])

    preg_test_result = models.CharField(
        verbose_name='What is the result of the pregnancy test?',
        max_length=10,
        choices=POS_NEG)

    comments = models.TextField(blank=True, null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Pregnancy Testing for Female Adolescents'
        verbose_name_plural = 'Pregnancy Testing for Female Adolescents'
