from django.db import models
from .list_models import ChronicConditions
from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins import ChildMedicalHistoryMixin


class ChildMedicalHistory(ChildCrfModelMixin,
                          ChildMedicalHistoryMixin):
    """A model completed by the user on Medical History for all children."""

    child_chronic = models.ManyToManyField(
        ChronicConditions,
        related_name='child',
        verbose_name=('Does the Child/Adolescent have any of the above. '
                      'Tick all that apply'), )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Children/Adolescents Medical History'
        verbose_name_plural = 'Children/Adolescents Medical History'
