from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import CBCL_SCALE


class ChildCBCLSection2(ChildCrfModelMixin):

    fear_harmful_thoughts = models.CharField(
        verbose_name='Fears he/she might think or do something bad',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(31)')

    fear_of_perfection = models.CharField(
        verbose_name='Feels he/she has to be perfect',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(32)')

    feels_unloved = models.CharField(
        verbose_name='Feels or complains that no one loves him/her',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(33)')

    feels_paranoia = models.CharField(
        verbose_name='Feels others are out to get him/her',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(34)')

    feels_worthless = models.CharField(
        verbose_name='Feels worthless or inferior',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(35)')

    accident_prone = models.CharField(
        verbose_name='Gets hurt a lot, accident-prone',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(36)')

    fights_involvement = models.CharField(
        verbose_name='Gets in many fights',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(37)')

    teased_alot = models.CharField(
        verbose_name='Gets teased a lot',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(38)')

    trouble_friends = models.CharField(
        verbose_name='Hangs around with others who get in trouble',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(39)')

    auditory_hallucination = models.CharField(
        verbose_name='Hears sounds or voices that aren\'t there',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(40)')

    ah_desc = models.TextField(
        verbose_name='Hears sounds or voices that aren\'t there (describe)',
        blank=True,
        null=True)

    impulsive = models.CharField(
        verbose_name='Impulsive of acts without thinking',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(41)')

    loner = models.CharField(
        verbose_name='Would rather be alone than with others',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(42)')

    cheating = models.CharField(
        verbose_name='Lying or cheating',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(43)')

    bites_nails = models.CharField(
        verbose_name='Bites fingernails',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(44)')

    nervousness = models.CharField(
        verbose_name='Nervous, highstrung, or tense',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(45)')

    nervous_moments = models.CharField(
        verbose_name='Nervous movements or twitching',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(46)')

    nervous_desc = models.TextField(
        verbose_name='Nervous movements or twitching (describe)',
        blank=True,
        null=True,)

    nightmares = models.CharField(
        verbose_name='Nightmares',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(47)')

    disliked_by_othrs = models.CharField(
        verbose_name='Not liked by other kids',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(48)')

    constipated = models.CharField(
        verbose_name='Constipated, doesn\'t move bowels',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(49)')

    anxiousness = models.CharField(
        verbose_name='Too fearful or anxious',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(50)')

    feels_dizzy = models.CharField(
        verbose_name='Feels dizzy or lightheaded',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(51)')

    feels_guity = models.CharField(
        verbose_name='Feels too guilty',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(52)')

    overeating = models.CharField(
        verbose_name='Overeating',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(53)')

    overtired_noreason = models.CharField(
        verbose_name='Overtired without good reason',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(54)')

    overweight = models.CharField(
        verbose_name='Overweight',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(55)')

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child CBCL Section: 2'
        verbose_name_plural = 'Child CBCL Section: 2'
