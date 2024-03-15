from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from flourish_caregiver.models.model_mixins import CaregiverSocialWorkReferralMixin
from flourish_caregiver.choices import CAREGIVER_OR_CHILD

from .list_models import ChildSocialWorkReferralList


class ChildSocialWorkReferral(ChildCrfModelMixin, CaregiverSocialWorkReferralMixin):

    referral_for = models.CharField(
        verbose_name='Referral For ',
        max_length=10,
        choices=CAREGIVER_OR_CHILD,
        default='child')

    referral_reason = models.ManyToManyField(
        ChildSocialWorkReferralList,
        verbose_name=('Please indicate reasons for the need for a social work '
                      'referral for the Mother/Caregiver or Child (select all that apply)'),
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child Referral'
        verbose_name_plural = 'Child Referral'
