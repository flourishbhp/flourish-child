from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import CBCL_SCALE


class ChildCBCLSection1(ChildCrfModelMixin):

    acts_young = models.CharField(
        verbose_name='Acts too young for his/her age',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(1)')

    unapproved_alc_intake = models.CharField(
        verbose_name='Drinks alcohol without parents\' approval',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(2)')

    alc_intake_desc = models.TextField(
        verbose_name='Drinks alcohol without parents\' approval (describe)',
        blank=True, null=True)

    argues_alot = models.CharField(
        verbose_name='Argues a lot',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(3)')

    fails_to_finish = models.CharField(
        verbose_name='Fails to finish things he/she starts',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(4)')

    enjoys_little = models.CharField(
        verbose_name='There is very little he/she enjoys',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(5)')

    bowel_incontinence = models.CharField(
        verbose_name='Bowel movements outside toilet',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(6)')

    bragging = models.CharField(
        verbose_name='Bragging, boasting',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(7)')

    attention_deficit = models.CharField(
        verbose_name='Can\'t concentrate, can\'t pay attention for long',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(8)')

    obssessive = models.CharField(
        verbose_name='Can\'t get his/her mind off certain thoughts; obsessions',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(9)')

    obssessive_desc = models.TextField(
        verbose_name='Can\'t get his/her mind off certain thoughts; obsessions (describe)',
        blank=True, null=True)

    hyperactive = models.CharField(
        verbose_name=' Can\'t sit still, restless, or hyperactive',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(10)')

    too_dependent = models.CharField(
        verbose_name='Clings to adults or too dependent',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(11)')

    feels_lonely = models.CharField(
        verbose_name='Complains of loneliness',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(12)')

    confused = models.CharField(
        verbose_name='Confused or seems to be in a fog',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(13)')

    cries_alot = models.CharField(
        verbose_name='Cries a lot',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(14)')

    animal_cruelty = models.CharField(
        verbose_name='Cruel to animals',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(15)')

    bullies_other = models.CharField(
        verbose_name='Cruelty, bullying, or meanness to others',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(16)')

    daydreams = models.CharField(
        verbose_name='Daydreams or gets lost in his/her thoughts',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(17)')

    self_harms = models.CharField(
        verbose_name='Deliberately harms self or attempts suicide',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(18)')

    demands_attention = models.CharField(
        verbose_name='Demands a lot of attention',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(19)')

    destroys_belongings = models.CharField(
        verbose_name='Destroys his/her own things',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(20)')

    destroys_othr_things = models.CharField(
        verbose_name='Destroys things belonging to his/her family or others',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(21)')

    disobedient_home = models.CharField(
        verbose_name='Disobedient at home',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(22)')

    disobedient_school = models.CharField(
        verbose_name='Disobedient at school',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(23)')

    eating_problems = models.CharField(
        verbose_name='Doesn\'t eat well',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(24)')

    unfitting = models.CharField(
        verbose_name='Doesn\'t get along with other kids',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(25)')

    unremorseful = models.CharField(
        verbose_name='Doesn\'t seem to feel guilty after misbehaving',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(26)')

    easily_jealous = models.CharField(
        verbose_name='Easily jealous',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(27)')

    breaks_rules = models.CharField(
        verbose_name='Breaks rules at home, school, or elsewhere',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(28)')

    fearful = models.CharField(
        verbose_name=('Fears certain animals, situations, or places, other than '
                      'school'),
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(29)')

    fearful_desc = models.TextField(
        verbose_name=('Fears certain animals, situations, or places, other than '
                      'school (describe)'),
        blank=True,
        null=True)

    fears_school = models.CharField(
        verbose_name='Fears going to school',
        choices=CBCL_SCALE,
        max_length=10,
        help_text='(30)')

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child CBCL Section: 1'
        verbose_name_plural = 'Child CBCL Section: 1'
