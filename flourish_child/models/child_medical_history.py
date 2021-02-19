from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from .list_models import ChronicConditions, WcsDxAdult
from .child_crf_model_mixin import ChildCrfModelMixin


class ChildMedicalHistory(ChildCrfModelMixin):

    """A model completed by the user on Medical History for all caregivers."""

    chronic_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name='Does the Child/Adolescent have any chronic conditions?', )

    child_chronic = models.ManyToManyField(
        ChronicConditions,
        related_name='child',
        verbose_name=('Does the Child/Adolescent have any of the above. '
                      'Tick all that apply'),)

    child_chronic_other = OtherCharField(
        max_length=35,
        verbose_name='If other, specify.',
        blank=True,
        null=True)

    who = models.ManyToManyField(
        WcsDxAdult,
        verbose_name='List any new WHO Stage III/IV diagnoses that are '
        'not reported'
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Children/Adolescents Medical History'
        verbose_name_plural = 'Children/Adolescents Medical History'
