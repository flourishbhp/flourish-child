from flourish_caregiver.models.model_mixins.flourish_tb_referral_mixin import \
    TBReferralMixin
from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin
from flourish_child.choices import TB_REFERRAL_REASON_CHOICES
from django.db import models
from .list_models import ChildTbReferralReasons


class ChildTBReferral(ChildCrfModelMixin, TBReferralMixin):
    reason_for_referral = models.ManyToManyField(
        ChildTbReferralReasons,
        related_name='reason_referral',
        verbose_name='Reason for referral:'
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent TB Referral'
        verbose_name_plural = 'Infant/Child/Adolescent TB Referrals'
