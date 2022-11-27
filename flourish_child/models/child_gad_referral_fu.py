from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins import ReferralFormFUMixin


class ChildGadReferralFU(ReferralFormFUMixin, ChildCrfModelMixin):

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child GAD-7 Referral Follow Up'
        verbose_name_plural = 'Child GAD-7 Referral Follow Up'
