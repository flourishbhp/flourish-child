from .child_crf_model_mixin import ChildCrfModelMixin
from flourish_caregiver.models.model_mixins import CaregiverSocialWorkReferralMixin


class ChildSocialWorkReferral(ChildCrfModelMixin, CaregiverSocialWorkReferralMixin):

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child Social Work Referral'
        verbose_name_plural = 'Child Social Work Referral'
