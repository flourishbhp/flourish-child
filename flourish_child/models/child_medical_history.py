from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO, POS_NEG
from edc_base.model_validators import date_not_future
from .list_models import ChronicConditions
from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import HIV_STATUS


class ChildMedicalHistory(ChildCrfModelMixin):

    """A model completed by the user on Medical History for all children."""

    chronic_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Does the Child/Adolescent have any chronic conditions?",
    )

    child_chronic = models.ManyToManyField(
        ChronicConditions,
        related_name="child",
        verbose_name=(
            "Does the Child/Adolescent have any of the above. " "Tick all that apply"
        ),
    )

    child_chronic_other = OtherCharField(
        max_length=35, verbose_name="If other, specify.", blank=True, null=True
    )

    """Quartely phone calls stem question"""
    med_history_changed = models.CharField(
        verbose_name="Has any of your following medical history changed?",
        max_length=20,
        choices=YES_NO,
        null=True,
    )

    current_hiv_status = models.CharField(
        verbose_name="What is the current HIV status of this infant/child/adolescent?",
        choices=HIV_STATUS,
        max_length=15,
        null=True,
        blank=True,
    )

    preg_test_performed = models.CharField(
        verbose_name="Was a pregnancy test performed?",
        max_length=3,
        choices=YES_NO,
    )

    pregnancy_test_result = models.CharField(
        verbose_name="What is the result of the pregnancy test?",
        max_length=20,
        choices=POS_NEG,
        blank=True,
        null=True,
    )
    
    last_menstrual_period = models.DateField(
        verbose_name="Date of Last Menstrual Period (DD/MMM/YYYY)",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    is_lmp_date_estimated = models.CharField(
        verbose_name="Is the Last Menstrual Period date estimated?",
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True,
    )

class Meta(ChildCrfModelMixin.Meta):
    app_label = "flourish_child"
    verbose_name = "Children/Adolescents Medical History"
    verbose_name_plural = "Children/Adolescents Medical History"
