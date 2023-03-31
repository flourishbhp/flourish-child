from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import CBCL_SCALE


class ChildCBCLSection3(ChildCrfModelMixin):

    # Physical problems without known medical cause
    body_aches = models.CharField(
        verbose_name='Aches or pains (not stomach or headaches)',
        choices=CBCL_SCALE,
        max_length=10)

    headaches = models.CharField(
        verbose_name='Headaches',
        choices=CBCL_SCALE,
        max_length=10)

    nauseous = models.CharField(
        verbose_name='Nausea, feels sick',
        choices=CBCL_SCALE,
        max_length=10)

    eye_prob = models.CharField(
        verbose_name='Problems with eyes (not if corrected by glasses',
        choices=CBCL_SCALE,
        max_length=10)

    eye_probl_desc = models.TextField(
         verbose_name='Problems with eyes (not if corrected by glasses (describe)',
         blank=True,
         null=True,
         max_length=500)

    skin_prob = models.CharField(
        verbose_name='Rashes or other skin problems',
        choices=CBCL_SCALE,
        max_length=10)

    stomach_aches = models.CharField(
        verbose_name='Stomach aches',
        choices=CBCL_SCALE,
        max_length=10)

    vomiting = models.CharField(
        verbose_name='Vomiting, throwing up',
        choices=CBCL_SCALE,
        max_length=10)

    other_phys_prob = models.CharField(
        verbose_name='Other (describe)',
        max_length=50)
    # End of section

    attacks_physical = models.CharField(
        verbose_name='Physically attacks people',
        choices=CBCL_SCALE,
        max_length=10)

    body_picking = models.CharField(
        verbose_name='Picks nose, skin, or other parts of body',
        choices=CBCL_SCALE,
        max_length=10)

    picking_desc = models.TextField(
        verbose_name='Picks nose, skin, or other parts of body (describe)',
        blank=True,
        null=True,
        max_length=500)

    sexparts_public_play = models.CharField(
        verbose_name='Plays with own sex parts in public',
        choices=CBCL_SCALE,
        max_length=10)

    sexparts_play = models.CharField(
        verbose_name='Plays with own sex parts too much',
        choices=CBCL_SCALE,
        max_length=10)

    poor_schoolwork = models.CharField(
        verbose_name='Poor school work',
        choices=CBCL_SCALE,
        max_length=10)

    clumsy = models.CharField(
        verbose_name='Poorly coordinated or clumsy',
        choices=CBCL_SCALE,
        max_length=10)

    prefers_older_kids = models.CharField(
        verbose_name='Prefers being with older kids',
        choices=CBCL_SCALE,
        max_length=10)

    prefers_young_kids = models.CharField(
        verbose_name='Prefers being with younger kids',
        choices=CBCL_SCALE,
        max_length=10)

    refuses_to_talk = models.CharField(
        verbose_name='Refuses to talk',
        choices=CBCL_SCALE,
        max_length=10)

    compulsions = models.CharField(
        verbose_name='Repeats certain acts over and over; compulsions',
        choices=CBCL_SCALE,
        max_length=10)

    compulsions_desc = models.TextField(
        verbose_name='Repeats certain acts over and over; compulsions (describe)',
        blank=True,
        null=True,
        max_length=500)

    home_runaway = models.CharField(
        verbose_name='Runs away from home',
        choices=CBCL_SCALE,
        max_length=10)

    screams_alot = models.CharField(
        verbose_name='Screams a lot',
        choices=CBCL_SCALE,
        max_length=10)

    secretive = models.CharField(
        verbose_name='Secretive, keeps things to self',
        choices=CBCL_SCALE,
        max_length=10)

    sight_hallucinations = models.CharField(
        verbose_name='Sees things that aren\'t there',
        choices=CBCL_SCALE,
        max_length=10)

    sh_desc = models.TextField(
        verbose_name='Sees things that aren\'t there (describe)',
        blank=True,
        null=True,
        max_length=500)

    self_conscious = models.CharField(
        verbose_name='Self-conscious or easily embarrassed',
        choices=CBCL_SCALE,
        max_length=10)

    sets_fires = models.CharField(
        verbose_name='Sets fires',
        choices=CBCL_SCALE,
        max_length=10)

    sexual_prob = models.CharField(
        verbose_name='Sexual problems',
        choices=CBCL_SCALE,
        max_length=10)

    sexual_prob_desc = models.TextField(
        verbose_name='Sexual problems (describe)',
        blank=True,
        null=True,
        max_length=500)

    showing_off = models.CharField(
        verbose_name='Showing off or clowning',
        choices=CBCL_SCALE,
        max_length=10)

    too_shy = models.CharField(
        verbose_name='Too shy or timid',
        choices=CBCL_SCALE,
        max_length=10)

    sleeps_less = models.CharField(
        verbose_name='Sleeps less than most kids',
        choices=CBCL_SCALE,
        max_length=10)

    sleeps_more = models.CharField(
        verbose_name='Sleeps more than most kids during day and/or night',
        choices=CBCL_SCALE,
        max_length=10)

    sleeps_more_desc = models.TextField(
        verbose_name='Sleeps more than most kids during day and/or night (describe)',
        blank=True,
        null=True,
        max_length=500)

    inattentive = models.CharField(
        verbose_name='Inattentive or easily distracted',
        choices=CBCL_SCALE,
        max_length=10)

    speech_prob = models.CharField(
        verbose_name='Speech problem',
        choices=CBCL_SCALE,
        max_length=10)

    speech_prob_desc = models.TextField(
        verbose_name='Speech problem (describe)',
        blank=True,
        null=True,
        max_length=500)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child CBCL Section: 3'
        verbose_name_plural = 'Child CBCL Section: 3'
