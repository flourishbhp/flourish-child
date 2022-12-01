
from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins import ReferralFormFUMixin


class ChildGadPostReferral(ReferralFormFUMixin, ChildCrfModelMixin):

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child GAD-7 Post Referral'
        verbose_name_plural = 'Child GAD-7 Post Referral'
