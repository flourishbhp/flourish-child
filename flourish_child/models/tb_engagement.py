from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import DECLINE_REASON, YES_NO_NOT_ELIGIBLE


class TbAdolEngagement(ChildCrfModelMixin):
    interview_consent = models.CharField(
        verbose_name='Is the participant interested in participating in the interview?',
        choices=YES_NO_NOT_ELIGIBLE,
        max_length=15, )

    interview_decline_reason = models.CharField(
        verbose_name='Provide reason for not undergoing the interview',
        choices=DECLINE_REASON,
        max_length=50,
        blank=True,
        null=True)

    interview_decline_reason_other = models.TextField(
        verbose_name='If other, specify',
        max_length=150,
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB Engagement'
