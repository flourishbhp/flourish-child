from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..choices import (
    WATER_SOURCE, COOKING_METHOD, TOILET_FACILITY, HOUSE_TYPE)
from ..choices import MONEY_PROVIDER, MONEY_EARNED
from ..choices import ETHNICITY, HIGHEST_EDUCATION

from .child_crf_model_mixin import ChildCrfModelMixin


class ChildSocioDemographic(ChildCrfModelMixin):

    """ A model completed by the user on Demographics form for all infants.
    """

    ethnicity = models.CharField(
        max_length=25,
        verbose_name="Ethnicity ",
        choices=ETHNICITY)

    ethnicity_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    highest_education = models.CharField(
        max_length=25,
        verbose_name="Highest educational level completed ",
        choices=HIGHEST_EDUCATION)

    provides_money = models.CharField(
        max_length=50,
        verbose_name="Who provides most of your money?",
        choices=MONEY_PROVIDER)

    provides_money_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    money_earned = models.CharField(
        max_length=50,
        verbose_name="How much money do you personally earn? ",
        choices=MONEY_EARNED)

    money_earned_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    own_phone = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Do you have your own cell phone that you use regularly?")

    water_source = models.CharField(
        max_length=50,
        verbose_name="At your primary home  where do you "
        "get most of your family's drinking water?",
        choices=WATER_SOURCE,
        help_text=("the home where you are likely to spend the"
                   " most time with your baby over the"
                   " first 18 months"),)

    house_electrified = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Is there electricity in this house / compound? ")

    house_fridge = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Is there a refrigerator being used in this house "
        "/ compound?  ")

    cooking_method = models.CharField(
        max_length=50,
        verbose_name="What is the primary method of cooking in this house "
        "/ compound?",
        choices=COOKING_METHOD)

    toilet_facility = models.CharField(
        max_length=50,
        verbose_name=("Which of the following types of toilet facilities do "
                      "you most often use"
                      " at this house / compound? "),
        choices=TOILET_FACILITY)

    toilet_facility_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,)

    house_people_number = models.IntegerField(
        verbose_name=("How many people, including yourself, stay in this home "
                      "/ compound most"
                      " of the time?"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100), ])

    house_type = models.CharField(
        max_length=50,
        verbose_name="Housing type?  ",
        choices=HOUSE_TYPE,
        help_text="Indicate the primary type of housing used over the past "
        "30 days",)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Child Sociodemographic Data"
        verbose_name_plural = "Child Sociodemographic Data"
