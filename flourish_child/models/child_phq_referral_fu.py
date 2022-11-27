from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins import ReferralFormFUMixin


class ChildPhqReferralFU(ReferralFormFUMixin, ChildCrfModelMixin):

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child PHQ-9 Referral Follow Up'
        verbose_name_plural = 'Child PHQ-9 Referral Follow Up'
