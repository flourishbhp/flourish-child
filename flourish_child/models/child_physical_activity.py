from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import (PHYS_ACTIVITY_TIME, VIGOROUS_ACTIVITY_DAYS,
                       MODERATE_ACTIVITY_DAYS, WALKING_DAYS)


class ChildPhysicalActivity(ChildCrfModelMixin):

    vig_activity_days = models.CharField(
        verbose_name=('During the last 7 days, on how many days did you do '
                      'vigorous physical activities like heavy lifting(carrying'
                      ' firewood, large buckets of water), digging, chopping '
                      'firewood, fast bicycling, sports(football, trackfield, etc'
                      ' ), or other activities where you are breathing hard '
                      'and exerting yourself?'),
        choices=VIGOROUS_ACTIVITY_DAYS,
        max_length=15)

    specify_vig_days = models.PositiveIntegerField(
        verbose_name='Specify days per week',
        validators=[MinValueValidator(1), MaxValueValidator(7), ],
        blank=True,
        null=True)

    vig_activity_time = models.CharField(
        verbose_name=('How much time did you usually spend doing vigorous '
                      'physical activities on one of those days?'),
        choices=PHYS_ACTIVITY_TIME,
        max_length=20,
        blank=True,
        null=True)

    specify_vig_time_hrs = models.PositiveIntegerField(
        verbose_name='Specify hours per day',
        validators=[MinValueValidator(1), MaxValueValidator(24), ],
        help_text='hours',
        blank=True,
        null=True)

    specify_vig_time_mins = models.PositiveIntegerField(
        verbose_name='Specify minutes per day',
        validators=[MinValueValidator(10), MaxValueValidator(60), ],
        help_text='minutes',
        blank=True,
        null=True)

    mod_activity_days = models.CharField(
        verbose_name=('During the last 7 days, on how many days did you do '
                      'moderate physical activities like carrying light loads,'
                      'bicycling at a regular/leisurely pace, or sports such as'
                      ' doubles tennis, badminton or shotput? Do not include walking.'),
        choices=MODERATE_ACTIVITY_DAYS,
        max_length=15)

    specify_mod_days = models.PositiveIntegerField(
        verbose_name='Specify days per week',
        validators=[MinValueValidator(1), MaxValueValidator(7), ],
        blank=True,
        null=True)

    mod_activity_time = models.CharField(
        verbose_name=('How much time did you usually spend doing moderate '
                      'physical activities on one of those days?'),
        choices=PHYS_ACTIVITY_TIME,
        max_length=16,
        blank=True,
        null=True)

    specify_mod_time_hrs = models.PositiveIntegerField(
        verbose_name='Specify hours per day',
        validators=[MinValueValidator(1), MaxValueValidator(24), ],
        help_text='hours',
        blank=True,
        null=True)

    specify_mod_time_mins = models.PositiveIntegerField(
        verbose_name='Specify minutes per day',
        validators=[MinValueValidator(0), MaxValueValidator(60), ],
        help_text='minutes',
        blank=True,
        null=True)

    walking_days = models.CharField(
        verbose_name=('During the last 7 days, on how many days did you walk '
                      'for at least 10 minutes at a time?'),
        choices=WALKING_DAYS,
        max_length=15,)

    specify_walk_days = models.PositiveIntegerField(
        verbose_name='Specify days per week',
        validators=[MinValueValidator(1), MaxValueValidator(7), ],
        blank=True,
        null=True)

    walking_time = models.CharField(
        verbose_name=('How much time did you usually spend walking on one of '
                      'those days?'),
        choices=PHYS_ACTIVITY_TIME,
        max_length=16,
        blank=True,
        null=True)

    specify_walk_time_hrs = models.PositiveIntegerField(
        verbose_name='Specify hours per day',
        validators=[MinValueValidator(1), MaxValueValidator(24), ],
        help_text='hours',
        blank=True,
        null=True)

    specify_walk_time_mins = models.PositiveIntegerField(
        verbose_name='Specify minutes per day',
        validators=[MinValueValidator(1), MaxValueValidator(60), ],
        help_text='minutes',
        blank=True,
        null=True)

    sitting_time = models.CharField(
        verbose_name=('During the last 7days, how much time did you spend '
                      'sitting on a week day?'),
        choices=PHYS_ACTIVITY_TIME,
        max_length=16,)

    specify_sit_time_hrs = models.PositiveIntegerField(
        verbose_name='Specify hours per day',
        validators=[MinValueValidator(1), MaxValueValidator(24), ],
        help_text='hours',
        blank=True,
        null=True)

    specify_sit_time_mins = models.PositiveIntegerField(
        verbose_name='Specify minutes per day',
        validators=[MinValueValidator(1), MaxValueValidator(60), ],
        help_text='minutes',
        blank=True,
        null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Physical Activity'
        verbose_name_plural = 'Physical Activities'
