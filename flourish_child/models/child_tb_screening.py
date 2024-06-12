from django.db import models

from flourish_caregiver.choices import YES_NO_AR_OTHER, YES_NO_UKN_CHOICES
from flourish_caregiver.helper_classes.tb_diagnosis import TBDiagnosis
from flourish_caregiver.models.model_mixins.flourish_tb_screening_mixin import \
    TBScreeningMixin
from flourish_child.choices import TEST_RESULTS_CHOICES, YES_NO_OTHER, YES_NO_UNKNOWN
from flourish_child.helper_classes.utils import child_utils
from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin


class ChildTBScreening(TBScreeningMixin, ChildCrfModelMixin):
    cough = models.CharField(
        verbose_name='Does your child currently have any cough?',
        choices=YES_NO_UKN_CHOICES,
        max_length=20)

    fever = models.CharField(
        verbose_name='Does your child currently have a fever?',
        choices=YES_NO_UKN_CHOICES,
        max_length=20)

    sweats = models.CharField(
        verbose_name='Is your child currently experiencing night sweats?',
        choices=YES_NO_UNKNOWN,
        help_text='Night sweats is defined as waking up with your bed clothing soaked – '
                  'enough to require the bed clothing to be changed',
        max_length=20)

    weight_loss = models.CharField(
        verbose_name='Since the last time you spoke with FLOURISH staff, has your child '
                     'had any weight loss (or no weight gain for a child who is less '
                     'than 12 years of age)?',
        choices=YES_NO_UKN_CHOICES,
        max_length=20, )

    fatigue_or_reduced_playfulness = models.CharField(
        verbose_name='Does your child have fatigue or reduced playfulness that has '
                     'lasted ≥2 weeks?',
        choices=YES_NO_UKN_CHOICES,
        max_length=20, )

    stool_sample_results = models.CharField(
        verbose_name='Stool Sample Results',
        choices=TEST_RESULTS_CHOICES,
        max_length=15, blank=True, null=True)

    child_diagnosed_with_tb = models.CharField(
        verbose_name='Was your child diagnosed with TB?',
        choices=YES_NO_AR_OTHER,
        max_length=20,
        blank=True, null=True)

    child_diagnosed_with_tb_other = models.TextField(
        verbose_name='If Other, please specify',
        blank=True, null=True)

    child_on_tb_treatment = models.CharField(
        verbose_name='Was your child started on TB treatment?',
        choices=YES_NO_OTHER,
        max_length=20,
        blank=True, null=True)

    child_on_tb_treatment_other = models.TextField(
        verbose_name='If Other, please specify',
        blank=True, null=True)

    child_on_tb_preventive_therapy = models.CharField(
        verbose_name='Was your child started on TB preventative therapy?',
        choices=YES_NO_OTHER,
        max_length=20,
        blank=True, null=True)

    child_on_tb_preventive_therapy_other = models.TextField(
        verbose_name='If Other, please specify',
        blank=True, null=True)

    evaluated_for_tb = models.CharField(
        verbose_name='Since the last time you spoke with FLOURISH staff, has your child '
                     'been evaluated in a clinic for TB? ',
        choices=YES_NO_UKN_CHOICES,
        max_length=20,
    )

    def save(self, *args, **kwargs):
        child_age = child_utils.child_age(self.child_visit.subject_identifier,
                                          self.report_datetime)
        tb_diagnoses = TBDiagnosis(child_age=child_age)
        self.tb_diagnoses = tb_diagnoses.evaluate_for_tb(self)

        super().save(*args, **kwargs)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant/Child/Adolescent TB Screening'
        verbose_name_plural = 'Infant/Child/Adolescent TB Screenings'
