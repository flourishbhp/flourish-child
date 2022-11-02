from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .child_crf_model_mixin import ChildCrfModelMixin


class AdolescentClinicalMeasurements(ChildCrfModelMixin):
    """ A model collected during the enrollment visit
    """

    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Adolescent\'s weight? ',
        validators=[MinValueValidator(20), MaxValueValidator(100), ],
        help_text='Measured in Kilograms (kg)')

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Adolescent\'s height? ',
        validators=[MinValueValidator(120), MaxValueValidator(200), ],
        null=True,
        blank=True,
        help_text='Measured in Centimeters (cm)')

    systolic_bp = models.IntegerField(
        verbose_name='Adolescent\'s systolic blood pressure?',
        validators=[MinValueValidator(50), MaxValueValidator(200), ],
        null=True,
        blank=True)

    diastolic_bp = models.IntegerField(
        verbose_name='Adolescent\'s diastolic blood pressure?',
        help_text='in hg e.g. 80, normal values are between 60 and 80.',
        null=True,
        blank=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Subject Anthropometric Data"
        verbose_name_plural = "Subject Anthropometric Data"
