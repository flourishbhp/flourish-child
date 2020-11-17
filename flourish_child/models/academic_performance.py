from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin

from ..choices import GRADE_LEVEL, MARKS


class AcademicPerformance(ChildCrfModelMixin):

    grade_level = models.CharField(
        verbose_name='What grade level are you in?',
        max_length=10,
        choices=GRADE_LEVEL)

    mathematics_marks = models.CharField(
        verbose_name='What are your marks in Mathematics?',
        max_length=20,
        choices=MARKS)

    reading_marks = models.CharField(
        verbose_name='What are your marks in Reading?',
        max_length=20,
        choices=MARKS)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Academic Performance'
        verbose_name_plural = 'Academic Performance'
