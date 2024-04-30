from django.db import models

from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_validators.date import date_not_future
from ..choices import YES_NO_UNKNOWN, YES_NO_UNKNOWN_NA, ARV_DRUG_LIST

from .child_crf_model_mixin import ChildCrfModelMixin


class InfantArvExposure(ChildCrfModelMixin):

    """ A model completed by the user on the infant's arv information.
        Version 2.0 - Added 14 Sep 2023, by adiphoko
    """

    azt_after_birth = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN,
        verbose_name="Did infant receive AZT syrup after birth?")

    azt_dose_date = models.DateField(
        verbose_name="If yes, date of first dose of AZT?",
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
        verbose_name="If yes Date of single dose NVP? ",
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

    """ Questions added later for version 2.0 of the form"""

    azt_within_72h = models.CharField(
        verbose_name='Did AZT dosing occur within 72 hours of birth',
        choices=YES_NO_UNKNOWN,
        max_length=10,
        null=True,
        blank=True)

    snvp_dose_within_72h = models.CharField(
        verbose_name='Did single dose NVP dosing occur within 72 hours of birth',
        choices=YES_NO_UNKNOWN,
        max_length=10,
        null=True,
        blank=True)

    nvp_cont_dosing = models.CharField(
        verbose_name=('Is NVP being prescribed for the infant to go '
                      'home on (continued dosing)'),
        choices=YES_NO_UNKNOWN,
        max_length=10,)

    additional_arvs = models.CharField(
         verbose_name=('Did the infant receive any additional ARVs within '
                       '72 hours of life?'),
        choices=YES_NO_UNKNOWN,
        max_length=10, )

    arvs_specify = models.CharField(
        verbose_name='Select the ARV',
        choices=ARV_DRUG_LIST,
        max_length=5,
        null=True,
        blank=True)

    arvs_specify_other = OtherCharField()

    date_1st_arv_dose = models.DateField(
        verbose_name='Date of first dosing of the ARV above',
        validators=[date_not_future, ],
        null=True,
        blank=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Infant ARV Exposure at Delivery"
        verbose_name_plural = "Infant ARV Exposure at Deliveries"
