from django.db import models

from ..choices import YES_NO_UNK_PNTA, \
    VISIT_NUMBER, HEALTH_CARE_CENTER, YES_NO_DN_PNTA, TB_SYMPTOM
from .child_crf_model_mixin import ChildCrfModelMixin
from .list_models import TbRoutineScreenAdolMedium
from edc_base.model_fields import OtherCharField



class TbRoutineScreenAdol(ChildCrfModelMixin):
    tb_health_visits = models.CharField(
        verbose_name='How many health visits did you have in the last year?',
        max_length=20,
        choices=VISIT_NUMBER,
        help_text='if 0, end of CRF else continue'
    )

    care_location = models.ManyToManyField(TbRoutineScreenAdolMedium,
        verbose_name='For visit #1, where did you receive care at?',
        help_text='if 0, end of CRF else continue',
        blank=True
    )

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
        verbose_name="At this visit, (specify service if multiple services within same visit),"
                     " were you screened for TB with the four screening"
                     " questions (cough, fever, weight loss, night sweats)?",
        choices=YES_NO_DN_PNTA,
        null=True,
        blank=True,
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

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Screen for TB at routine health encounters'
        verbose_name_plural = 'Screen for TB at routine health encounters'
