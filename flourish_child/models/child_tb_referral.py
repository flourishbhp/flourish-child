from flourish_caregiver.models.model_mixins.flourish_tb_referral_mixin import \
    TBReferralMixin
from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin


class ChildTBReferral(ChildCrfModelMixin, TBReferralMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent TB Referral'
        verbose_name_plural = 'Infant/Child/Adolescent TB Referrals'
