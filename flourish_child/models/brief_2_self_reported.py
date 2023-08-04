from django.db import models
from edc_constants.choices import YES_NO

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import BRIEF2_SCALE, CBCL_IMPACT, CBCL_INTEREST, CBCL_INVALID_REASON, \
    CBCL_UNDERSTANDING


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

    brief2_self_interest = models.CharField(
        verbose_name='For BRIEF-2 Screening Self-Report Form how interested was the '
                     'child/adolescent?',
        choices=CBCL_INTEREST,
        max_length=30,
        blank=True,
        null=True)

    brief2_self_understanding = models.CharField(
        verbose_name='For this test, how well did the child/adolescent understand the '
                     'questions being asked?',
        choices=CBCL_UNDERSTANDING,
        max_length=30,
        blank=True,
        null=True)

    brief2_self_valid = models.CharField(
        verbose_name='In your opinion, are the results of the Brief-2 self-report valid?',
        choices=YES_NO,
        max_length=10,
        blank=True,
        null=True)

    brief2_self_invalid_reason = models.CharField(
        verbose_name='If the test was NOT VALID, specify the reason why it was not '
                     'valid:',
        choices=CBCL_INVALID_REASON,
        max_length=100,
        blank=True,
        null=True)

    brief2_self_impact_on_responses = models.CharField(
        verbose_name='Did any of the following impact responses to the Brief-2 '
                     'questions:',
        choices=CBCL_IMPACT,
        max_length=50,
        blank=True,
        null=True)

    brief2_self_overall_comments = models.TextField(
        verbose_name='Overall comments for the Brief 2 Self-Report:',
        max_length=1000,
        blank=True,
        null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'BRIEF-2 Screening Self-Reported'
        verbose_name_plural = 'BRIEF-2 Screening Self-Reported'
