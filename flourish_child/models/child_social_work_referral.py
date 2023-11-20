from .child_crf_model_mixin import ChildCrfModelMixin
from flourish_caregiver.models.model_mixins import CaregiverSocialWorkReferralMixin
from django.db import models
from flourish_caregiver.choices import CAREGIVER_OR_CHILD


class ChildSocialWorkReferral(ChildCrfModelMixin, CaregiverSocialWorkReferralMixin):

    referral_for = models.CharField(
        verbose_name='Referral For ',
        max_length=10,
        choices=CAREGIVER_OR_CHILD,
        default='child')

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child Social Work Referral'
        verbose_name_plural = 'Child Social Work Referral'
