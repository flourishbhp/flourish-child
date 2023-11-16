from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from flourish_caregiver.models.model_mixins import CaregiverSocialWorkReferralMixin

from .list_models import ChildSocialWorkReferralList


class ChildSocialWorkReferral(ChildCrfModelMixin, CaregiverSocialWorkReferralMixin):

    referral_reason = models.ManyToManyField(
        ChildSocialWorkReferralList,
        verbose_name=('Please indicate reasons for the need for a social work '
                      'referral for the Mother/Caregiver or Child (select all that apply)'),
        blank=True
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child Social Work Referral'
        verbose_name_plural = 'Child Social Work Referral'
