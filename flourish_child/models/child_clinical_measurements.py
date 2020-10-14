from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .child_crf_model_mixin import ChildCrfModelMixin


class ChildClinicalMeasurements(ChildCrfModelMixin):
    """ A model completed by the user on Height, Weight details
    for all infant/child/adolescent. """

    child_height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Infant/child/adolescent's height? ",
        validators=[MinValueValidator(114), MaxValueValidator(195), ],
        help_text="Measured in Centimeters (cm)")

    child_weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Infant/child/adolescent's weight? ",
        validators=[MinValueValidator(30), MaxValueValidator(136), ],
        help_text="Measured in Kilograms (kg)")

    child_systolic_bp = models.IntegerField(
        verbose_name="Infant/child/adolescent's systolic blood pressure?",
        validators=[MinValueValidator(75), MaxValueValidator(220), ],
        help_text="in mm e.g. 120, should be between 75 and 220."
    )

    child_diastolic_bp = models.IntegerField(
        verbose_name="Infant/child/adolescent's diastolic blood pressure?",
        validators=[MinValueValidator(35), MaxValueValidator(150), ],
        help_text="in hg e.g. 80, should be between 35 and 150.")

    child_waist_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Infant/child/adolescent\'s waist circumference',
        validators=[MinValueValidator(15), MaxValueValidator(420), ],
        help_text='')

    child_hip_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Infant/child/adolescent\'s hip circumference',
        validators=[MinValueValidator(15), MaxValueValidator(420), ],
        help_text='')

    child_skin_folds = models.CharField(
        verbose_name='Infant/child/adolescent skin folds',
        max_length=100)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent Clinical Measurements'
        verbose_name_plural = 'Infant/Child/Adolescent Clinical Measurements'
