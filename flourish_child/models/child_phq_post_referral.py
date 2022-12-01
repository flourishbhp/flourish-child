
from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins import ReferralFormFUMixin


class ChildPhqPostReferral(ReferralFormFUMixin, ChildCrfModelMixin):

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child PHQ-9 Post Referral'
        verbose_name_plural = 'Child PHQ-9 Post Referral'
