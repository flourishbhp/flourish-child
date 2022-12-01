from django.db import models

from ..choices import EMO_SUPPORT_PROVIDER
from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins import ReferralFormFUMixin


class ChildPhqReferralFU(ReferralFormFUMixin, ChildCrfModelMixin):

    emo_support_provider = models.CharField(
        verbose_name=('You mentioned that you are currently receiving emotional '
                      'support services. Do you mind sharing with us where you are receiving '
                      'these services?'),
        max_length=40,
        choices=EMO_SUPPORT_PROVIDER)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child PHQ-9 Referral Follow Up'
        verbose_name_plural = 'Child PHQ-9 Referral Follow Up'
