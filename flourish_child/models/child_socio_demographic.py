from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from ..choices import (
    WATER_SOURCE, COOKING_METHOD, TOILET_FACILITY, HOUSE_TYPE,
    HIGHEST_EDUCATION)
from ..choices import ETHNICITY, SCHOOL_TYPE

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

    stay_with_caregiver = models.CharField(
        verbose_name='Is the infant/child/adolescent currently living with '
                     'the caregiver who is also participating in the FLOURISH'
                     ' study?',
        choices=YES_NO,
        max_length=3)

    water_source = models.CharField(
        max_length=50,
        verbose_name='At this child\'s primary home / compound where do you '
                     'get most of the drinking water?',
        choices=WATER_SOURCE)

    house_electrified = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name='Is there electricity at the child\'s primary home / '
                     'compound?')

    house_fridge = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=('Is there a refrigerator being used in the child\'s '
                      'primary home / compound?'))

    cooking_method = models.CharField(
        max_length=50,
        verbose_name='What is the primary method of cooking in the child\'s '
                     'primary home / compound?',
        choices=COOKING_METHOD)

    toilet_facility = models.CharField(
        max_length=50,
        verbose_name='Which of the following types of toilet facilities do '
                     'you most often use at the child\'s primary home / '
                     'compound?',
        choices=TOILET_FACILITY)

    toilet_facility_other = OtherCharField(
        max_length=35,
        verbose_name='If other specify...',
        blank=True,
        null=True,)

    house_people_number = models.IntegerField(
        verbose_name='How many household members live in the child\'s primary'
                     ' home  / compound ?',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(25), ],
        help_text='A household member is considered someone who spends more '
                  'nights on average in your household than in any other '
                  'household in the same community over the last 12 months.')

    house_type = models.CharField(
        max_length=50,
        verbose_name='Housing type?',
        choices=HOUSE_TYPE,
        help_text='Indicate the primary type of housing used over the past '
                  '30 days')

    older_than18 = models.IntegerField(
        verbose_name='Of the people who live in this household, how many are '
                     'older than 18?',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(25), ],)

    attend_school = models.CharField(
        verbose_name='Is the infant/child/adolescent attending school?',
        max_length=7,
        choices=YES_NO)

    education_level = models.CharField(
        verbose_name='What level/class of school is the child currently in?',
        max_length=20,
        choices=HIGHEST_EDUCATION,
        default='no_schooling')

    education_level_other = OtherCharField(
        verbose_name='Specify other',
        blank=True,
        null=True,
        max_length=30)

    school_type = models.CharField(
        verbose_name='What type of school does this child attend?',
        choices=SCHOOL_TYPE,
        max_length=15,
        default=NOT_APPLICABLE)

    working = models.CharField(
        verbose_name='Is this adolescent currently working in return '
                     'for cash?',
        max_length=7,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    """Quartely phone calls stem question"""
    socio_demo_changed = models.CharField(
        verbose_name='Has any of your following socio demographic data changed?',
        max_length=3,
        choices=YES_NO,
        null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Child Sociodemographic Data"
        verbose_name_plural = "Child Sociodemographic Data"
