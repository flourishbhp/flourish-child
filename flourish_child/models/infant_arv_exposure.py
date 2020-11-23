from django.db import models

from edc_base.model_validators.date import date_not_future
from ..choices import YES_NO_UNKNOWN, YES_NO_UNKNOWN_NA

from .child_crf_model_mixin import ChildCrfModelMixin


class InfantArvExposure(ChildCrfModelMixin):

    """ A model completed by the user on the infant's arv information. """

    azt_after_birth = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Did infant receive AZT syrup after birth?")

    azt_dose_date = models.DateField(
        verbose_name="If yes,date of first dose of AZT?",
        validators=[date_not_future, ],
        blank=True,
        null=True)

    azt_additional_dose = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN_NA,
        verbose_name="Was the infant given additional doses of AZT before discharge from the hospital? ",
        help_text=("if insufficient timing from delivery to next required dose"
                   " has elapsed, please enter 'Not applicable'"))

    sdnvp_after_birth = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Did the infant receive single dose NVP after birth? ",
        help_text="")

    nvp_dose_date = models.DateField(
        verbose_name="If yes Date of first Dose NVP? ",
        validators=[date_not_future, ],
        blank=True,
        null=True)

    azt_discharge_supply = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN_NA,
        verbose_name="Was the infant discharged with a supply of AZT? ",
        help_text="if infant not yet discharged, please enter 'Not applicable'")

    infant_arv_comments = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information ",
        blank=True,
        null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Infant ARV Exposure"
        verbose_name_plural = "Infant ARV Exposure"
