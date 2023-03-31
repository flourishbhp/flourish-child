from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import ANSWERER, FOOD, HOW_OFTEN, YES_NO_DONT_KNOW


class ChildFoodSecurityQuestionnaire(ChildCrfModelMixin):

    answerer = models.CharField(
        verbose_name='Who will answer the Food Security Questionnaire?',
        max_length=30, choices=ANSWERER)

    did_food_last = models.CharField(
        verbose_name='The food that (I/we) bought just didn’t last, and (I/we)'
                     ' didn’t have money to get more.',
        max_length=70, choices=FOOD)

    balanced_meals = models.CharField(
        verbose_name='(I/we) couldn\'t afford to eat balanced meals.',
        max_length=70, choices=FOOD)

    cut_meals = models.CharField(
        verbose_name='In the last 12 months, since last (name of current '
                     'month), did (you/you or other adults in your household) '
                     'ever cut the size of your meals or skip meals because '
                     'there wasn\'t enough money for food?',
        max_length=70, choices=YES_NO_DONT_KNOW)

    how_often = models.CharField(
        verbose_name='How often did this happen?',
        blank=True, null=True,
        max_length=60, choices=HOW_OFTEN)

    eat_less = models.CharField(
        verbose_name='In the last 12 months, did you ever eat less than you '
                     'felt you should because there wasn\'t enough money for'
                     ' food?',
        max_length=20, choices=YES_NO_DONT_KNOW)

    didnt_eat = models.CharField(
        verbose_name='In the last 12 months, were you every hungry but didn\'t'
                     ' eat because there wasn\'t enough money for food?',
        max_length=20, choices=YES_NO_DONT_KNOW)

    class Meta(ChildCrfModelMixin.Meta):

        app_label = 'flourish_child'
        verbose_name = 'Children/Adolescents Food Security Questionnaire'
        verbose_name_plural = 'Children/Adolescents Food Security ' \
                              'Questionnaire'
