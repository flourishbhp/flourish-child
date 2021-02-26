from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin

from ..choices import HIGHEST_EDUCATION, MARKS, NUMBER_OF_DAYS
from edc_base.model_fields import OtherCharField


class AcademicPerformance(ChildCrfModelMixin):

    education_level = models.CharField(
        verbose_name='Highest level of school completed',
        max_length=20,
        choices=HIGHEST_EDUCATION)

    education_level_other = OtherCharField(
        verbose_name='Specify other',
        blank=True,
        null=True,
        max_length=30)

    mathematics_marks = models.CharField(
        verbose_name='What are your marks in Mathematics?',
        max_length=20,
        choices=MARKS)

    reading_marks = models.CharField(
        verbose_name='What are your marks in Reading?',
        max_length=20,
        choices=MARKS)

    history_marks = models.CharField(
        verbose_name='What are your marks in History?',
        max_length=20,
        choices=MARKS)
    num_days = models.CharField(
        verbose_name='How many days a week do you attend in-peron classes?',
        max_length=10,
        choices=NUMBER_OF_DAYS)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Academic Performance'
        verbose_name_plural = 'Academic Performance'
