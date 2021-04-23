from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin


class ChildBirthScreening(ChildCrfModelMixin):

    weight = models.DecimalField(
        verbose_name='Birth weight (kg)',
        decimal_places=2, max_digits=10)

    length = models.DecimalField(
        verbose_name='Length',
        decimal_places=2, max_digits=10)

    gestational_age = models.IntegerField(
        verbose_name='Gestational Age at birth')

    arv_exposure = models.CharField(
        verbose_name='I have blamed myself unnecessarily when '
                     'things went wrong',
        max_length=50)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Birth Weight/Length'
        verbose_name_plural = 'Birth Weight/Length'
