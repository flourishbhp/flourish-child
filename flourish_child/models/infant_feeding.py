from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_validators.date import date_not_future
from edc_constants.choices import YES_NO, YES_NO_UNSURE, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from ..choices import (WATER_USED, FREQUENCY_BREASTMILK_REC, BF_ESTIMATED,
                       COWS_MILK)
from .child_crf_model_mixin import ChildCrfModelMixin
from .list_models import SolidFoods


class InfantFeeding(ChildCrfModelMixin):

    """ A model completed by the user on the infant's feeding. """

    last_att_sche_visit = models.DateField(
        verbose_name=('The last infant feeding form was completed on '),
        null=True)

    """Quartely Phone call stem question"""
    infant_feeding_changed = models.CharField(
        verbose_name=('Since the last scheduled visit, has any of your '
                      'following infant feeding information changed?'),
        choices=YES_NO,
        max_length=3,
        null=True)

    ever_breastfed = models.CharField(
        verbose_name=('Has the participant ever breast fed? '),
        max_length=3,
        choices=YES_NO)

    bf_start_dt = models.DateField(
        verbose_name='Date start of breast feeding',
        validators=[date_not_future],
        blank=True,
        null=True)

    bf_start_dt_est = models.CharField(
        verbose_name='Is the start date of breast feeding estimated?',
        max_length=30,
        choices=BF_ESTIMATED,
        blank=True,
        null=True)

    recent_bf_dt = models.DateField(
        verbose_name='Date of most recent beast feeding',
        blank=True,
        null=True)

    continuing_to_bf = models.CharField(
        verbose_name='Is the participant continuing to breast feed',
        max_length=3,
        choices=YES_NO,
        blank=True,
        null=True)

    child_weaned = models.CharField(
        verbose_name='Is the participant completely weaned from breast milk?',
        max_length=3,
        choices=YES_NO,
        blank=True,
        null=True,
        help_text=('Atleast 72 hours without breast feeding, no intention to re-start'))

    dt_weaned = models.DateField(
        verbose_name=('If no longer breast feeding, please provide the date '
                      'of the participant weaned'),
        blank=True,
        null=True)

    freq_milk_rec = models.CharField(
        verbose_name=('On average, how often did the participant receive breast'
                      ' milk for feeding?'),
        max_length=100,
        choices=FREQUENCY_BREASTMILK_REC,
        default=NOT_APPLICABLE)

    rec_liquids = models.CharField(
        verbose_name=('Has the participant received any liquids other than '
                      'breast milk?'),
        max_length=3,
        choices=YES_NO)

    took_formula = models.CharField(
        verbose_name='Has the infant taken formula?',
        max_length=10,
        choices=YES_NO_UNSURE,
        blank=True,
        null=True)

    formula_first_report = models.CharField(
        verbose_name=('Is this the first reporting of infant formula use?'),
        max_length=3,
        choices=YES_NO_NA)

    dt_formula_introduced = models.DateField(
        verbose_name='Date infant formula introduced',
        blank=True,
        null=True)

    dt_formula_est = models.CharField(
        verbose_name='Is date infant formula introduced estimated?',
        max_length=20,
        choices=YES_NO,
        blank=True,
        null=True)

    formula_feedng_completd = models.CharField(
        verbose_name='Has the infant completed formula feeding?',
        max_length=3,
        choices=YES_NO,
        blank=True,
        null=True)

    dt_formula_stopd = models.DateField(
        verbose_name='Date of when infant formula was stopped',
        blank=True,
        null=True)

    dt_stopd_est = models.CharField(
        verbose_name='Is the date infant formula stopped estimated?',
        max_length=20,
        choices=YES_NO,
        blank=True,
        null=True)

    formula_water = models.CharField(
        verbose_name=('What water do you usually use to prepare the '
                      'participant\'s infant formula?'),
        max_length=50,
        choices=WATER_USED,
        default=NOT_APPLICABLE)

    formula_water_other = OtherCharField(
        verbose_name='If \'Other\', specify',
        max_length=35,
        blank=True,
        null=True)

    taken_water = models.CharField(
        verbose_name='Has the infant taken water?',
        max_length=10,
        choices=YES_NO_UNSURE,
        help_text='Not as part of formula milk.',
        blank=True,
        null=True)

    taken_juice = models.CharField(
        verbose_name='Has the infant taken juice?',
        max_length=10,
        choices=YES_NO_UNSURE,
        blank=True,
        null=True)

    taken_cows_milk = models.CharField(
        verbose_name='Has the infant taken cow\'s milk?',
        max_length=10,
        choices=YES_NO_UNSURE,
        blank=True,
        null=True)

    cows_milk_prep = models.CharField(
        verbose_name='If \'Yes\', cow\'s milk was...',
        max_length=10,
        choices=COWS_MILK,
        default=NOT_APPLICABLE)

    taken_animal_milk = models.CharField(
        verbose_name='Has the infant taken other animal milk?',
        max_length=10,
        choices=YES_NO_UNSURE,
        blank=True,
        null=True)

    animal_milk_specify = models.CharField(
        verbose_name='If \'Yes\' specify which animal',
        max_length=50,
        blank=True,
        null=True)

    milk_boiled = OtherCharField(
        verbose_name='Was milk boiled?',
        max_length=10,
        choices=YES_NO_UNSURE,
        blank=True,
        null=True)

    taken_salts = models.CharField(
        verbose_name='Has the infant taken oral rehydration salts?',
        max_length=10,
        choices=YES_NO_UNSURE,
        blank=True,
        null=True)

    taken_solid_foods = models.CharField(
        verbose_name='Has the infant received any solid foods?',
        max_length=3,
        choices=YES_NO)

    """Solid Food Section"""

    solid_foods_dt = models.DateField(
        verbose_name='Date the participant first started receiving solids',
        blank=True,
        null=True)

    solid_foods_age = models.IntegerField(
        verbose_name=('At approximately what age, in months, did this child '
                      'start taking solid foods (foods other than breast '
                      'milk or formula)?'),
        blank=True,
        null=True)

    provide_response_solid = models.CharField(
        verbose_name=('Are you able to provide answers about solid foods and '
                      'their frequency the child/infant is taking?'),
        max_length=20,
        choices=YES_NO,
        blank=True,
        null=True)

    solid_foods = models.ManyToManyField(
        SolidFoods,
        verbose_name='What solid foods is your infant/child taking?',
        help_text='(tick all that apply)',
        blank=True)

    solid_foods_past_week = models.ManyToManyField(
        SolidFoods,
        related_name='solid_foods_past_week',
        verbose_name='What solid foods did your child take in the past week (past seven days)',
        help_text='(tick all that apply)',
        blank=True)

    grain_intake_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'Grains, roots and tubers'),
        blank=True,
        null=True)

    legumes_intake_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'Legumes and nuts'),
        blank=True,
        null=True)

    dairy_intake_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'Dairy products (milk, yogurt, cheese)'),
        blank=True,
        null=True)

    flesh_foods_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'Flesh foods (meat, fish, poultry and liver/organ meat)'),
        blank=True,
        null=True)

    eggs_intake_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'Eggs'),
        blank=True,
        null=True)

    porridge_intake_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'Porridge'),
        blank=True,
        null=True)

    vitamin_a_fruits_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'Vitamin A rich fruits and vegetables (carrots)'),
        blank=True,
        null=True)

    other_fruits_vegies = models.CharField(
        verbose_name=('Please describe other types of fruits and vegetables '
                      'the infant/child is taking(most common)'),
        max_length=150,
        blank=True,
        null=True)

    other_fruits_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'Other fruits and vegetables'),
        blank=True,
        null=True)

    other_solids = models.CharField(
        verbose_name=('Please describe other types of solid foods the infant/'
                      'child is taking'),
        max_length=150,
        blank=True,
        null=True)

    other_solids_freq = models.IntegerField(
        verbose_name=('In the past week how many times a week did this child take '
                      'the other foods'),
        blank=True,
        null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant Feeding'
        verbose_name_plural = 'Infant Feeding'
