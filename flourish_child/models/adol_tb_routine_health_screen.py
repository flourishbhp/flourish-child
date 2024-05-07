from django.db import models

from ..choices import (YES_NO_UNK_PNTA, VISIT_NUMBER, YES_NO_DN_PNTA,
                       TB_SYMPTOM, TB_DIAGONISTIC_TYPE, YES_NO_PENDING_UNK)

from .child_crf_model_mixin import ChildCrfModelMixin
from .list_models import TbRoutineScreenAdolMedium
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel


class TbRoutineScreenAdol(ChildCrfModelMixin):
    tb_health_visits = models.CharField(
        verbose_name='How many health visits did you have in the last year?',
        max_length=20,
        choices=VISIT_NUMBER,
        help_text='if 0, end of CRF else continue'
    )

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB screen during routine encounters'
        verbose_name_plural = 'TB screen during routine encounters'


class TbHealthVisitAdol(BaseUuidModel):
    tb_screenin = models.ForeignKey(
        TbRoutineScreenAdol,
        on_delete=models.DO_NOTHING)

    care_location = models.ManyToManyField(
        TbRoutineScreenAdolMedium,
        verbose_name='Where did you receive care at this healthcare visit?',
        help_text='if 0, end of CRF else continue',
        blank=False)

    care_location_other = OtherCharField(
        verbose_name='If ‘other’, specify',
    )

    visit_reason = models.CharField(
        verbose_name='What was the primary reason for your health visit?',
        max_length=33,
        null=True,
        blank=True,
        choices=TB_SYMPTOM
    )

    visit_reason_other = OtherCharField(
        verbose_name='If ‘other’, specify',
    )

    screening_questions = models.CharField(
        verbose_name=('At this visit, (specify service if multiple services '
                      'within same visit), were you screened for TB with the'
                      ' four screening questions (cough, fever, weight loss,'
                      'night sweats)?'),
        choices=YES_NO_DN_PNTA,
        max_length=20,
        help_text='if yes continue to Q7 '
                  'if no/I do not know/prefer not to answer, '
                  'CRF complete if no further visits, else repeat questions'
                  ' 2-8 for each healthcare visit reported in question 1 '
    )

    pos_screen = models.CharField(
        verbose_name='Did you screen positive for TB at this visit'
                     ' (specify service if multiple services within same '
                     'visit),  because you had cough, fever, weight loss, and/or night sweats?',
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_UNK_PNTA,
        help_text='If no/ I do not know /prefer not to answer,'
                  ' CRF complete if no further visits, else repeat '
                  'questions 2-8 for each healthcare visit reported in question 1 '

    )

    diagnostic_referral = models.CharField(
        verbose_name='Were you referred for TB diagnostic evaluation?',
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_UNK_PNTA)

    diagnostic_studies = models.CharField(
        verbose_name='What diagnostic studies were performed?',
        choices=TB_DIAGONISTIC_TYPE,
        max_length=20,
        null=True,
        blank=True,
    )

    diagnostic_studies_other = OtherCharField(
        verbose_name='other, specify'
    )

    tb_diagnostic = models.CharField(
        verbose_name='Where any of the TB diagnostic studies positive?',
        max_length=20,
        choices=YES_NO_PENDING_UNK,
        null=True,
        blank=True,
    )

    specify_tests = models.TextField(
        verbose_name='Specify test and test results',
        null=True,
        blank=True,
    )

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB Adol. Screening Healthy Visit'
        verbose_name_plural = 'TB Adol. Screening Healthy Visits'
