from django.db import models
from edc_constants.choices import YES_NO
from flourish_caregiver.models.model_mixins.flourish_tb_referral_outcome_mixin import \
    FlourishTbReferralOutcomeMixin
from flourish_child.choices import TB_TREATMENT_CHOICES, TEST_RESULTS_CHOICES, \
    YES_NO_OTHER
from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin
from flourish_child.models.list_models import ChildTBTests


class ChildTBReferralOutcome(ChildCrfModelMixin, FlourishTbReferralOutcomeMixin):
    stool_sample_results = models.CharField(
        verbose_name='Stool Sample Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    tests_performed = models.ManyToManyField(
        ChildTBTests,
        verbose_name='What diagnostic tests were performed for TB',
        blank=True)

    diagnosed_with_tb = models.CharField(
        verbose_name='Was your child diagnosed with TB?',
        choices=YES_NO,
        max_length=3, blank=True, null=True)

    tb_treatment = models.CharField(
        verbose_name='Was your child started on TB treatment?',
        choices=TB_TREATMENT_CHOICES,
        max_length=20, blank=True, null=True)

    tb_preventative_therapy = models.CharField(
        verbose_name='Was your child started on TB preventative therapy?treatment ('
                     'consists of'
                     'four or more drugs taken over several months)',
        choices=YES_NO_OTHER,
        max_length=10, blank=True, null=True)
    tb_isoniazid_preventative_therapy = models.CharField(
        verbose_name='Was your child started on TB preventative therapy (such as '
                     'isoniazid or'
                     'rifapentine/isoniazid for several months)? ',
        choices=YES_NO_OTHER,
        max_length=10, blank=True, null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent TB Referral Outcomes CRF'
        verbose_name_plural = 'Infant/Child/Adolescent TB Referral Outcomes CRFs'
