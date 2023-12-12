from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import CBCL_SCALE


class ChildCBCLSection3(ChildCrfModelMixin):

    # Physical problems without known medical cause
    body_aches = models.CharField(
        verbose_name='Aches or pains (not stomach or headaches)',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(56, a.)')

    headaches = models.CharField(
        verbose_name='Headaches',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(56, b.)')

    nauseous = models.CharField(
        verbose_name='Nausea, feels sick',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(56, c.)')

    eye_prob = models.CharField(
        verbose_name='Problems with eyes (not if corrected by glasses)',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(56, d.)')

    eye_probl_desc = models.TextField(
         verbose_name='Problems with eyes (not if corrected by glasses (describe)',
         blank=True,
         null=True,)

    skin_prob = models.CharField(
        verbose_name='Rashes or other skin problems',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(56, e.)')

    stomach_aches = models.CharField(
        verbose_name='Stomach aches',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(56, f.)')

    vomiting = models.CharField(
        verbose_name='Vomiting, throwing up',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(56, g.)')

    other_phys_prob = models.CharField(
        verbose_name='Other (describe)',
        max_length=50,
        help_text='(56, h.)')
    # End of section

    attacks_physical = models.CharField(
        verbose_name='Physically attacks people',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(57)')

    body_picking = models.CharField(
        verbose_name='Picks nose, skin, or other parts of body',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(58)')

    picking_desc = models.TextField(
        verbose_name='Picks nose, skin, or other parts of body (describe)',
        blank=True,
        null=True,)

    sexparts_public_play = models.CharField(
        verbose_name='Plays with own sex parts in public',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(59)')

    sexparts_play = models.CharField(
        verbose_name='Plays with own sex parts too much',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(60)')

    poor_schoolwork = models.CharField(
        verbose_name='Poor school work',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(61)')

    clumsy = models.CharField(
        verbose_name='Poorly coordinated or clumsy',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(62)')

    prefers_older_kids = models.CharField(
        verbose_name='Prefers being with older kids',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(63)')

    prefers_young_kids = models.CharField(
        verbose_name='Prefers being with younger kids',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(64)')

    refuses_to_talk = models.CharField(
        verbose_name='Refuses to talk',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(65)')

    compulsions = models.CharField(
        verbose_name='Repeats certain acts over and over; compulsions',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(66)')

    compulsions_desc = models.TextField(
        verbose_name='Repeats certain acts over and over; compulsions (describe)',
        blank=True,
        null=True,)

    home_runaway = models.CharField(
        verbose_name='Runs away from home',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(67)')

    screams_alot = models.CharField(
        verbose_name='Screams a lot',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(68)')

    secretive = models.CharField(
        verbose_name='Secretive, keeps things to self',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(69)')

    sight_hallucinations = models.CharField(
        verbose_name='Sees things that aren\'t there',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(70)')

    sh_desc = models.TextField(
        verbose_name='Sees things that aren\'t there (describe)',
        blank=True,
        null=True,)

    self_conscious = models.CharField(
        verbose_name='Self-conscious or easily embarrassed',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(71)')

    sets_fires = models.CharField(
        verbose_name='Sets fires',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(72)')

    sexual_prob = models.CharField(
        verbose_name='Sexual problems',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(73)')

    sexual_prob_desc = models.TextField(
        verbose_name='Sexual problems (describe)',
        blank=True,
        null=True,)

    showing_off = models.CharField(
        verbose_name='Showing off or clowning',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(74)')

    too_shy = models.CharField(
        verbose_name='Too shy or timid',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(75)')

    sleeps_less = models.CharField(
        verbose_name='Sleeps less than most kids',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(76)')

    sleeps_more = models.CharField(
        verbose_name='Sleeps more than most kids during day and/or night',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(77)')

    sleeps_more_desc = models.TextField(
        verbose_name='Sleeps more than most kids during day and/or night (describe)',
        blank=True,
        null=True,)

    inattentive = models.CharField(
        verbose_name='Inattentive or easily distracted',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(78)')

    speech_prob = models.CharField(
        verbose_name='Speech problem',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(79)')

    speech_prob_desc = models.TextField(
        verbose_name='Speech problem (describe)',
        blank=True,
        null=True,)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child CBCL Section: 3'
        verbose_name_plural = 'Child CBCL Section: 3'
