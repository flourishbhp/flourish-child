from django.db import models

from flourish_caregiver.models.model_mixins.flourish_tb_referral_outcome_mixin import \
    FlourishTbReferralOutcomeMixin
from flourish_child.choices import TEST_RESULTS_CHOICES
from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin
from flourish_child.models.list_models import ChildTBTests


class ChildTBReferralOutcome(ChildCrfModelMixin, FlourishTbReferralOutcomeMixin):
    
    tests_performed = models.ManyToManyField(
        ChildTBTests,
        verbose_name='What diagnostic tests were performed for TB',
        blank=True, )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent TB Referral Outcomes CRF'
        verbose_name_plural = 'Infant/Child/Adolescent TB Referral Outcomes CRFs'
