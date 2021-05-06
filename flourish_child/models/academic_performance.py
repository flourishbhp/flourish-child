from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin

from ..choices import MARKS, NUMBER_OF_DAYS, OVERALL_MARKS
from edc_base.model_fields import OtherCharField


class AcademicPerformance(ChildCrfModelMixin):

    education_level = models.CharField(
        verbose_name='What level/class of school is the child currently in?',
        max_length=20)

    education_level_other = OtherCharField(
        verbose_name='Specify other',
        max_length=30)

    mathematics_marks = models.CharField(
        verbose_name='What are your marks in Mathematics?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    science_marks = models.CharField(
        verbose_name='What are your marks in Science?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    setswana_marks = models.CharField(
        verbose_name='What are your marks in Setswana?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    english_marks = models.CharField(
        verbose_name='What are your marks in English?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    physical_edu_marks = models.CharField(
        verbose_name='What are your marks in Physical Education?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    cultural_stds_marks = models.CharField(
        verbose_name='What are your marks in Cultural Studies?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    social_stds_marks = models.CharField(
        verbose_name='What are your marks in Social Studies?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    agriculture_marks = models.CharField(
        verbose_name='What are your marks in Agriculture?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    single_scie_marks = models.CharField(
        verbose_name='What are your marks in Single Science?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    biology_marks = models.CharField(
        verbose_name='What are your marks in Biology?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    chemistry_marks = models.CharField(
        verbose_name='What are your marks in Chemistry?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    physics_marks = models.CharField(
        verbose_name='What are your marks in Physics?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    double_scie_marks = models.CharField(
        verbose_name='What are your marks in Double Science?',
        max_length=20,
        choices=MARKS,
        default='not_taking_subject')

    overall_performance = models.CharField(
        verbose_name='What is your overall performance in your last examination?',
        max_length=20,
        choices=OVERALL_MARKS)

    num_days = models.CharField(
        verbose_name='How many days a week do you attend in-peron classes?',
        max_length=10,
        choices=NUMBER_OF_DAYS)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Academic Performance'
        verbose_name_plural = 'Academic Performance'
