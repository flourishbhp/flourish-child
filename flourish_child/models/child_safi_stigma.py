from django.db import models
from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import (PERIOD_HAPPENED, HAPPENED,
                       PERIOD_HAPPENED_DONT_KNOW, HAPPENED_DONT_KNOW)


class ChildSafiStigma(ChildCrfModelMixin):

    lost_friends = models.CharField(
        verbose_name='Because someone else in my family has HIV, I have lost friends',
        max_length=20,
        choices=HAPPENED
    )

    lost_friends_period = models.CharField(
        verbose_name='If "Ever happened" : when',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True
    )

    bullied = models.CharField(
        verbose_name='Because someone else in my family has HIV, I have been called names, insulted, or bullied',
        max_length=20,
        choices=HAPPENED
    )

    bullied_period = models.CharField(
        verbose_name='If "Ever happened" : when',
        choices=PERIOD_HAPPENED,
        max_length=20,
        blank=True,
        null=True
    )

    home_discr = models.CharField(
        verbose_name='Home',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    home_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    neighborhood_discr = models.CharField(
        verbose_name='Neighborhood',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    neighborhood_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    religious_place_discr = models.CharField(
        verbose_name=' A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    religious_place_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    clinic_discr = models.CharField(
        verbose_name='Clinic',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    clinic_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    school_discr = models.CharField(
        verbose_name='School',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    school_discr_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    other_place_discr = models.CharField(
        verbose_name='Other Place',
        max_length=100,
        blank=True,
        null=True
    )

    other_place_discr_period = models.CharField(
        verbose_name='If “Ever Happened” at Other Place: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    lose_fin_support = models.CharField(
        verbose_name='Lose Financial Support/Work',
        max_length=20,
        choices=HAPPENED
    )

    lose_fin_support_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    lose_social_support = models.CharField(
        verbose_name='Lose Social Support',
        max_length=20,
        choices=HAPPENED
    )

    lose_social_support_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    stressed_or_anxious = models.CharField(
        verbose_name='Stressed or anxious',
        max_length=20,
        choices=HAPPENED,
    )

    stressed_or_anxious_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    depressed_or_sad = models.CharField(
        verbose_name='Depressed, feeling down, saddened ',
        max_length=20,
        choices=HAPPENED,
    )

    depressed_or_sad_period = models.CharField(
        verbose_name='If “Ever Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child SAFI Stigma'
        verbose_name_plural = 'Child SAFI Stigma'
