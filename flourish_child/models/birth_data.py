from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import YES

from .child_crf_model_mixin import ChildCrfModelMixin
from ..helper_classes.utils import child_utils


class BirthData(ChildCrfModelMixin):
    """ A model completed by the user on the infant's birth exam. """

    weight_avail = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name='Is the infant\'s birth weight available?',
        default=YES)

    weight_kg = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="What was the infant's birth weight? ",
        help_text="Measured in Kilograms (kg)",
        blank=True,
        null=True)

    length_avail = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name='Is the infant\'s length at birth available?',
        default=YES)

    infant_length = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(11), MaxValueValidator(125)],
        verbose_name="What was the infant's length at birth? ",
        help_text="Measured in centimeters, (cm)",
        blank=True,
        null=True)

    head_circ_avail = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name='Is the infant\'s head circumference at birth available?',
        default=YES)

    head_circumference = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(11), MaxValueValidator(54)],
        verbose_name="What was the head circumference in centimeters? ",
        help_text="Measured in centimeters, (cm)",
        blank=True,
        null=True)

    apgar_score = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was Apgar Score performed? ",
        help_text="If 'No' go to question 10. Otherwise continue")

    gestational_age = models.DecimalField(
        verbose_name="What is the infant's determined gestational age: ",
        max_digits=5,
        decimal_places=2,
    )

    apgar_score_min_1 = models.IntegerField(
        verbose_name="At 1 minute: ",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)])

    apgar_score_min_5 = models.IntegerField(
        verbose_name="At 5 minutes: ",
        blank=True,
        null=True,
        validators=[MaxValueValidator(10),
                    MinValueValidator(0)])

    apgar_score_min_10 = models.IntegerField(
        verbose_name="At 10 minutes: ",
        blank=True,
        null=True,
        validators=[MaxValueValidator(10),
                    MinValueValidator(0)])

    congenital_anomalities = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Were any congenital anomalies identified? ",
        help_text="If 'Yes' please complete the Congenital Anomalies Form",)

    other_birth_info = models.TextField(
        max_length=250,
        verbose_name="Other birth information ",
        blank=True,
        null=True)

    def save(self, *args, **kwargs):
        subject_identifier = getattr(
            self.child_visit, 'subject_identifier', None)
        if not self.gestational_age:
            self.gestational_age = child_utils.get_gestational_age(
                subject_identifier)
        super().save(*args, **kwargs)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Birth Data"
        verbose_name_plural = "Birth Data"
