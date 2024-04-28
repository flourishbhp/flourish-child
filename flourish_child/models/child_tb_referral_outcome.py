from django.db import models
from edc_constants.choices import YES_NO
from flourish_caregiver.models.model_mixins.flourish_tb_referral_outcome_mixin import \
    FlourishTbReferralOutcomeMixin
from flourish_child.choices import TB_TREATMENT_CHOICES, TEST_RESULTS_CHOICES, \
    YES_NO_OTHER
from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin
from flourish_child.models.list_models import ChildTBTests
from flourish_caregiver.choices import NO_EVALUATION_REASONS


class ChildTBReferralOutcome(ChildCrfModelMixin, FlourishTbReferralOutcomeMixin):
    stool_sample_results = models.CharField(
        verbose_name='Stool Sample Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    tests_performed = models.ManyToManyField(
        ChildTBTests,
        verbose_name='What diagnostic tests were performed for TB',
        blank=True)
    
    evaluated = models.CharField(
        verbose_name='Was the child evaluated at the clinic?',
        choices=YES_NO,
        max_length=30,
        blank=True, null=True)
    
    reason_not_evaluated = models.CharField(
        verbose_name='Reasons that child was not evaluated at the clinic',
        choices=NO_EVALUATION_REASONS,
        max_length=30,
        blank=True, null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent TB Referral Outcomes CRF'
        verbose_name_plural = 'Infant/Child/Adolescent TB Referral Outcomes CRFs'
