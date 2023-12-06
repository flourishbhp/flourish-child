from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins.test_questions_mixin import TestQuestionMixin
from ..choices import CBCL_SCALE


class ChildCBCLSection4(ChildCrfModelMixin, TestQuestionMixin):
    stares_blankly = models.CharField(
        verbose_name='Stares blankly',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(80)')

    steals_at_home = models.CharField(
        verbose_name='Steals at home',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(81)')

    steals_elsewhere = models.CharField(
        verbose_name='Steals outside the home',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(82)')

    hoarding = models.CharField(
        verbose_name='Stores up too many things he/she doesn\'t need',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(83)')

    hoarding_desc = models.TextField(
        verbose_name='Stores up too many things he/she doesn\'t need (describe)',
        blank=True,
        null=True,)

    strange_behavior = models.CharField(
        verbose_name='Strange behavior',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(84)')

    behavior_desc = models.TextField(
        verbose_name='Strange behavior (describe)',
        blank=True,
        null=True,)

    strange_ideas = models.CharField(
        verbose_name='Strange ideas',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(85)')

    ideas_desc = models.TextField(
        verbose_name='Strange ideas (describe)',
        blank=True,
        null=True,)

    irritable = models.CharField(
        verbose_name='Stubborn, sullen, or irritable',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(86)')

    sudden_mood_chng = models.CharField(
        verbose_name='Sudden changes in mood or feelings',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(87)')

    sulks_alot = models.CharField(
        verbose_name='Sulks a lot',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(88)')

    suspicious = models.CharField(
        verbose_name='Suspicious',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(89)')

    swearing = models.CharField(
        verbose_name='Swearing or obscene language',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(90)')

    self_harm_talks = models.CharField(
        verbose_name='Talks about killing self',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(91)')

    sleepwalk_talk = models.CharField(
        verbose_name='Talks or walks in sleep',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(92)')

    sleepwalk_desc = models.TextField(
        verbose_name='Talks or walks in sleep (describe)',
        blank=True,
        null=True,)

    talks_alot = models.CharField(
        verbose_name='Talks too much',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(93)')

    teases_alot = models.CharField(
        verbose_name='Teases a lot',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(94)')

    hot_temper = models.CharField(
        verbose_name='Temper tantrum or hot temper ',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(95)')

    sex_thoughts = models.CharField(
        verbose_name='Thinks about sex too much',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(96)')

    threatens_people = models.CharField(
        verbose_name='Threatens people',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(97)')

    thumbsucking = models.CharField(
        verbose_name='Thumb-sucking',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(98)')

    smokes = models.CharField(
        verbose_name='Smokes, chews, sniffs tobacco or uses e-cigs',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(99)')

    trouble_sleeping = models.CharField(
        verbose_name='Trouble sleeping',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(100)')

    sleeping_desc = models.TextField(
        verbose_name='Trouble sleeping (describe)',
        blank=True,
        null=True,)

    skips_school = models.CharField(
        verbose_name='Truancy, skips school',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(101)')

    underactive = models.CharField(
        verbose_name='Underactive, slow moving, or lacks energy',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(102)')

    unhappy = models.CharField(
        verbose_name='Unhappy, sad, or depressed',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(103)')

    unusually_loud = models.CharField(
        verbose_name='Unusually loud',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(104)')

    drug_usage = models.CharField(
        verbose_name='Uses drugs for nonmedical purposes (don\'t include alcohol or '
                     'tobacco)',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(105)')

    drug_usage_desc = models.TextField(
        verbose_name=(
            'Uses drugs for nonmedical purposes (don\'t include alcohol or tobacco)'
            ' (describe)'),
        blank=True,
        null=True,)

    vandalism = models.CharField(
        verbose_name='Vandalism',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(106)')

    daytime_wetting = models.CharField(
        verbose_name='Wets self during the day',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(107)')

    bedtime_wetting = models.CharField(
        verbose_name='Wets the bed',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(108)')

    whining = models.CharField(
        verbose_name='Whining',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(109)')

    gender_dissonant = models.CharField(
        verbose_name='Wishes to be of opposite sex',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(110)')

    withdrawn = models.CharField(
        verbose_name='Withdrawn, doesn\'t get invovled with others',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(111)')

    worries = models.CharField(
        verbose_name='Worries',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(112)')

    other_problems = models.TextField(
        verbose_name='Please write in any problems your child has that were not listed above',
        help_text='(113)')

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child CBCL Section: 4'
        verbose_name_plural = 'Child CBCL Section: 4'
