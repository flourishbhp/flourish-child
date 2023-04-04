from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import BRIEF2_SCALE


class Brief2SelfReported(ChildCrfModelMixin):

    short_attention_span = models.CharField(
        verbose_name='I have a short attention span',
        choices=BRIEF2_SCALE,
        max_length=10)

    task_completion_prob = models.CharField(
        verbose_name='I have difficulty finishing a task on my own',
        choices=BRIEF2_SCALE,
        max_length=10)

    bothered_by_change = models.CharField(
        verbose_name=('It bothers me when I have to deal with changes '
                      '(such as routines, foods, or places)'),
        choices=BRIEF2_SCALE,
        max_length=10)

    no_planning = models.CharField(
        verbose_name=('I don’t plan ahead for school assignments'),
        choices=BRIEF2_SCALE,
        max_length=10)

    impulsive = models.CharField(
        verbose_name=('I am impulsive (I don\'t think before doing)'),
        choices=BRIEF2_SCALE,
        max_length=10)

    poor_writing = models.CharField(
        verbose_name='I have problems organizing my written work',
        choices=BRIEF2_SCALE,
        max_length=10)

    stuck_on_activty = models.CharField(
        verbose_name='I get stuck on one topic or activity',
        choices=BRIEF2_SCALE,
        max_length=10)

    easily_upset = models.CharField(
        verbose_name='I get upset over small events',
        choices=BRIEF2_SCALE,
        max_length=10)

    overreact = models.CharField(
        verbose_name='I overreact',
        choices=BRIEF2_SCALE,
        max_length=10)

    forgetful = models.CharField(
        verbose_name='I forget instructions easily',
        choices=BRIEF2_SCALE,
        max_length=10)

    delayed_task_completion = models.CharField(
        verbose_name='It takes me longer to complete my work',
        choices=BRIEF2_SCALE,
        max_length=10)

    delayed_task_completion = models.CharField(
        verbose_name='It takes me longer to complete my work',
        choices=BRIEF2_SCALE,
        max_length=10)

    unthinking = models.CharField(
        verbose_name='I don’t think of consequences before acting',
        choices=BRIEF2_SCALE,
        max_length=10)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'BRIEF-2 Screening Self-Reported'
        verbose_name_plural = 'BRIEF-2 Screening Self-Reported'
