from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .child_crf_model_mixin import ChildCrfModelMixin


class AdolescentClinicalMeasurements(ChildCrfModelMixin):
    """ A model collected during the enrollment visit
    """

    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Weight(kg)? ',
        validators=[MinValueValidator(20), MaxValueValidator(100), ],
        help_text='Measured in Kilograms (kg)')

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Height(cm)? ',
        validators=[MinValueValidator(120), MaxValueValidator(200), ],
        help_text='Measured in Centimeters(cm)')

    systolic_bp = models.IntegerField(
        verbose_name='Systolic blood pressure(BP)?',
        validators=[MinValueValidator(50), MaxValueValidator(200), ],
        help_text='Should be between 50 and 200',)

    diastolic_bp = models.IntegerField(
        verbose_name='Diastolic blood pressure(BP)?',
        help_text='Should be between 40 and 120',
        validators=[MinValueValidator(40), MaxValueValidator(120), ],)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Anthropometrics"
        verbose_name_plural = "Subject Anthropometric Data"
