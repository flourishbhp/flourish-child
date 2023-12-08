from django.db import models
from edc_constants.constants import YES
from edc_base.model_fields import OtherCharField
from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import (PERIOD_HAPPENED, HAPPENED,
                       PERIOD_HAPPENED_DONT_KNOW, HAPPENED_DONT_KNOW, HIV_PERSPECTIVE)


class ChildSafiStigma(ChildCrfModelMixin):

    lost_friends = models.CharField(
        verbose_name='Because someone else in my family has HIV, I have lost friends',
        max_length=20,
        choices=HAPPENED
    )

    lost_friends_happened_when = models.CharField(
        verbose_name='If "Ever happened" : when',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True
    )

    discriminated = models.CharField(
        verbose_name='Because someone else in my family has HIV, I have been called names, insulted, or bullied',
        max_length=20,
        choices=HAPPENED
    )

    discriminated_when = models.CharField(
        verbose_name='If "Ever happened" : when',
        choices=PERIOD_HAPPENED,
        max_length=20,
        blank=True,
        null=True
    )

    child_home_discrimination = models.CharField(
        verbose_name='Home',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    child_home_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    child_neighborhood_discrimination = models.CharField(
        verbose_name='Neighborhood',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    child_neighborhood_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    child_religious_place_discrimination = models.CharField(
        verbose_name=' A Religious Place (e.g. church)',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    child_religious_place_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    child_clinic_discrimination = models.CharField(
        verbose_name='Clinic',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    child_clinic_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    child_school_discrimination = models.CharField(
        verbose_name='School',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    child_school_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW,
        blank=True,
        null=True,
    )

    child_other_discrimination = models.CharField(
        verbose_name='Other Place',
        max_length=20,
        choices=HAPPENED_DONT_KNOW,
    )

    child_other_discrimination_other = OtherCharField()

    child_other_discrimination_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED_DONT_KNOW
    )

    lose_finacial_support = models.CharField(
        verbose_name='Lose Financial Support/Work',
        max_length=20,
        choices=HAPPENED
    )

    lose_finacial_support_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
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
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    stressed_or_anxious = models.CharField(
        verbose_name='Lose Social Support',
        max_length=20,
        choices=HAPPENED,

    )

    stressed_or_anxious_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    depressed_or_saddened = models.CharField(
        verbose_name='Depressed, feeling down, saddened ',
        max_length=20,
        choices=HAPPENED,
    )

    depressed_or_saddened_period = models.CharField(
        verbose_name='If “Even Happened”: When?',
        max_length=20,
        choices=PERIOD_HAPPENED,
        blank=True,
        null=True,
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child SAFI Stigma'
        verbose_name_plural = 'Child SAFI Stigma'
