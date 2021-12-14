from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from .child_crf_model_mixin import ChildCrfModelMixin


class ChildClinicalMeasurements(ChildCrfModelMixin):
    """ A model completed by the user on Height, Weight details
    for all infant/child/adolescent. """

    child_weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Infant/child/adolescent's weight? ",
        help_text="Measured in Kilograms (kg)")

    child_systolic_bp = models.IntegerField(
        verbose_name="Infant/child/adolescent's systolic blood pressure?",
        validators=[MinValueValidator(50), MaxValueValidator(200), ],
        blank=True,
        null=True,
        help_text="in mm e.g. 120, should be between 50 and 200."
    )

    child_diastolic_bp = models.IntegerField(
        verbose_name="Infant/child/adolescent's diastolic blood pressure?",
        validators=[MinValueValidator(40), MaxValueValidator(120), ],
        blank=True,
        null=True,
        help_text="in hg e.g. 80, should be between 40 and 120.")

    child_height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Infant/child/adolescent's height? ",
        help_text="Measured in Centimeters (cm)")

    is_child_preg = models.CharField(
        verbose_name='Is the child pregnant?',
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    child_waist_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Infant/child/adolescent\'s waist circumference',
        validators=[MinValueValidator(15), MaxValueValidator(200), ],
        help_text='in cm e.g 20, should be between 15 and 200')

    child_hip_circ = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Infant/child/adolescent\'s hip circumference',
        validators=[MinValueValidator(15), MaxValueValidator(420), ],
        help_text='in cm e.g 20, should be between 15 and 420')

    skin_folds_triceps = models.DecimalField(
        verbose_name='Infant/child/adolescent skin folds measurement at triceps',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(45), ],
        blank=True,
        null=True,
        help_text='in mm e.g 2, should be between 1 and 45')

    skin_folds_subscapular = models.DecimalField(
        verbose_name='Infant/child/adolescent skin folds measurement at subscapular',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(45), ],
        blank=True,
        null=True,
        help_text='in mm e.g 2, should be between 1 and 45')

    skin_folds_suprailiac = models.DecimalField(
        verbose_name='Infant/child/adolescent skin folds measurement at suprailiac crest',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(55), ],
        blank=True,
        null=True,
        help_text='in mm e.g 2, should be between 1 and 55')

    child_muac = models.DecimalField(
        verbose_name='Infant/child/adolescent MUAC measurement',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(5), MaxValueValidator(50), ],
        help_text='in cm e.g 2, should be between 5 and 50')

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent Clinical Measurements'
        verbose_name_plural = 'Infant/Child/Adolescent Clinical Measurements'
