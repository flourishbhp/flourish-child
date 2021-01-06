from django.core.validators import MinValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA

from ..choices import (
    KNOW_HIV_STATUS, LOWEST_CD4_KNOWN, IS_DATE_ESTIMATED)
from .list_models import ChronicConditions, ChildMedications, WcsDxAdult
from .child_crf_model_mixin import ChildCrfModelMixin


class ChildMedicalHistory(ChildCrfModelMixin):

    """ A model completed by the user on Medical History for all
    child/adolescent. """

    chronic_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name='Does the child/adolescent have any chronic conditions?'
    )

    who_diagnosis = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name='Prior to the current pregnancy, was the participant ever'
        ' diagnosed with a WHO Stage III or IV illness?',
        help_text='Please use the WHO Staging Guidelines. ONLY for HIV '
        'infected child/adolescent'
    )

    who = models.ManyToManyField(
        WcsDxAdult,
        verbose_name='List any new WHO Stage III/IV diagnoses that are '
        'not reported'
    )

    child_chronic = models.ManyToManyField(
        ChronicConditions,
        related_name='mother',
        verbose_name='Does the child/adolescent have any of the above. Tick '
                     'all that apply',
    )

    child_chronic_other = OtherCharField(
        max_length=35,
        verbose_name='if other, specify.',
        blank=True,
        null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Children/Adolescents Medical History'
        verbose_name_plural = 'Children/Adolescents Medical History'
