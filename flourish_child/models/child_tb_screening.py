from django.db import models
from edc_constants.choices import YES_NO

from flourish_caregiver.models.model_mixins.flourish_tb_screening_mixin import \
    TBScreeningMixin
from flourish_child.choices import TEST_RESULTS_CHOICES
from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin


class ChildTBScreening(TBScreeningMixin, ChildCrfModelMixin):
    fatigue_or_reduced_playfulness = models.CharField(
        verbose_name='Does your child have fatigue or reduced playfulness that has '
                     'lasted ≥2 weeks?',
        choices=YES_NO,
        max_length=3, )

    stool_sample_results = models.CharField(
        verbose_name='Stool Sample Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    child_diagnosed_with_tb = models.CharField(
        verbose_name='Was your child diagnosed with TB?',
        choices=YES_NO,
        max_length=3,
        blank=True, null=True)

    child_on_tb_treatment = models.CharField(
        verbose_name='Was your child started on TB treatment?',
        choices=YES_NO,
        max_length=3,
        blank=True, null=True)

    child_on_tb_preventive_therapy = models.CharField(
        verbose_name='Was your child started on TB preventative therapy?',
        choices=YES_NO,
        max_length=3,
        blank=True, null=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent TB Screening'
        verbose_name_plural = 'Infant/Child/Adolescent TB Screenings'
