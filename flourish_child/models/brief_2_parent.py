from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import BRIEF2_SCALE


class Brief2Parent(ChildCrfModelMixin):

    memory_retention = models.CharField(
        verbose_name='When given three things to do, remembers only the first or last',
        choices=BRIEF2_SCALE,
        max_length=10)

    lacks_follow_through = models.CharField(
        verbose_name='Has good ideas but does not get job done (lacks follow-through)',
        choices=BRIEF2_SCALE,
        max_length=10)

    task_completion_prob = models.CharField(
        verbose_name='Has trouble finishing tasks (chores, homework, etc.)',
        choices=BRIEF2_SCALE,
        max_length=10)

    out_of_control = models.CharField(
        verbose_name='Gets out of control more than friends',
        choices=BRIEF2_SCALE,
        max_length=10)

    stronger_reactions = models.CharField(
        verbose_name='Reacts more strongly to situations than other children',
        choices=BRIEF2_SCALE,
        max_length=10)

    no_planning = models.CharField(
        verbose_name='Does not plan ahead for school assignments',
        choices=BRIEF2_SCALE,
        max_length=10)

    poor_writing = models.CharField(
        verbose_name='Written work is poorly organized',
        choices=BRIEF2_SCALE,
        max_length=10)

    action_breaks = models.CharField(
        verbose_name='Has trouble putting the breaks on his/her actions',
        choices=BRIEF2_SCALE,
        max_length=10)

    unaware_of_others = models.CharField(
        verbose_name='Does not realize that certain actions bother others',
        choices=BRIEF2_SCALE,
        max_length=10)

    easily_triggered = models.CharField(
        verbose_name='Small events trigger big reactions',
        choices=BRIEF2_SCALE,
        max_length=10)

    trouble_moving_on = models.CharField(
        verbose_name='Has trouble moving from one activity to another',
        choices=BRIEF2_SCALE,
        max_length=10)

    stuck_on_activty = models.CharField(
        verbose_name='Gets stuck on one topic or activity',
        choices=BRIEF2_SCALE,
        max_length=10)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'BRIEF-2 Screening Parent'
        verbose_name_plural = 'BRIEF-2 Screening Parent'
