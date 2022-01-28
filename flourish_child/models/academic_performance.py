from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..choices import HIGHEST_EDUCATION, MARKS, NUMBER_OF_DAYS, OVERALL_MARKS
from .child_crf_model_mixin import ChildCrfModelMixin


class AcademicPerformance(ChildCrfModelMixin):

    education_level = models.CharField(
        choices=HIGHEST_EDUCATION,
        verbose_name="What level/class of school is the child currently in?",
        max_length=20,
    )

    education_level_other = OtherCharField(verbose_name="Specify other", max_length=30)

    mathematics_marks = models.CharField(
        verbose_name="What are your marks in Mathematics?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    science_marks = models.CharField(
        verbose_name="What are your marks in Science?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    setswana_marks = models.CharField(
        verbose_name="What are your marks in Setswana?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    english_marks = models.CharField(
        verbose_name="What are your marks in English?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    physical_edu_marks = models.CharField(
        verbose_name="What are your marks in Physical Education?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    cultural_stds_marks = models.CharField(
        verbose_name="What are your marks in Cultural Studies?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    social_stds_marks = models.CharField(
        verbose_name="What are your marks in Social Studies?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    agriculture_marks = models.CharField(
        verbose_name="What are your marks in Agriculture?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    single_scie_marks = models.CharField(
        verbose_name="What are your marks in Single Science?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    biology_marks = models.CharField(
        verbose_name="What are your marks in Biology?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    chemistry_marks = models.CharField(
        verbose_name="What are your marks in Chemistry?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    physics_marks = models.CharField(
        verbose_name="What are your marks in Physics?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    double_scie_marks = models.CharField(
        verbose_name="What are your marks in Double Science?",
        max_length=25,
        choices=MARKS,
        default="not_taking_subject",
    )

    overall_performance = models.CharField(
        verbose_name="What is your overall performance in your last examination?",
        max_length=25,
        choices=OVERALL_MARKS,
    )

    grade_points = models.PositiveIntegerField(
        verbose_name="Overall grade points", blank=True, null=True
    )

    num_days = models.CharField(
        verbose_name="How many days a week do you attend in-person classes?",
        max_length=10,
        choices=NUMBER_OF_DAYS,
    )

    """Quartely phone calls stem question"""
    academic_perf_changed = models.CharField(
        verbose_name=(
            "Has any of your subject marks or overall performance in your last "
            "examination changed?"
        ),
        max_length=3,
        choices=YES_NO,
        null=True,
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = "flourish_child"
        verbose_name = "Academic Performance"
        verbose_name_plural = "Academic Performance"
