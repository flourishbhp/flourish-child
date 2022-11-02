from django.db import models

from ..choices import YES_NO_UNK_DWTA, \
    VISIT_NUMBER, HEALTH_CARE_CENTER, YES_NO_DN_PNTA, VISIT_REASON
from .child_crf_model_mixin import ChildCrfModelMixin


class TbRoutineScreenAdolescent(ChildCrfModelMixin):
    tb_health_visits = models.CharField(
        verbose_name='How many health visits did you have in the last year?',
        max_length=20,
        choices=VISIT_NUMBER,
        help_text='if 0, end of CRF else continue'
    )

    care_location = models.CharField(
        verbose_name='For visit #1, where did you receive care at?',
        max_length=100,
        choices=HEALTH_CARE_CENTER,
        help_text='if 0, end of CRF else continue'
    )

    other = models.TextField(
        verbose_name='If ‘other’, specify: (free text)',
        null=True,
        blank=True,
    )

    visit_reason = models.CharField(
        verbose_name='What was the primary reason for your health visit?',
        max_length=30,
        null=True,
        blank=True,
        choices=VISIT_REASON
    )

    screening_questions = models.CharField(
        verbose_name="At this visit, (specify service if multiple services within same visit),"
                     " were you screened for TB with the four screening"
                     " questions (cough, fever, weight loss, night sweats)?",
        choices=YES_NO_DN_PNTA,
        max_length=20,
        help_text="f no/I do not know/prefer not to answer, "
                  "CRF complete if no further visits, else repeat questions"
                  " 2-8 for each healthcare visit reported in question 1 "
    )

    pos_screen = models.CharField(
        verbose_name='Did you screen positive for the TB symptom screen?',
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_UNK_DWTA)

    diagnostic_referral = models.CharField(
        verbose_name='Were you referred for TB diagnostic evaluation?',
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_UNK_DWTA)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Screen for TB at routine health encounters'
        verbose_name_plural = 'Screen for TB at routine health encounters'
