from django.db import models
from edc_constants.choices import YES_NO
from edc_base.model_fields import OtherCharField

from ..choices import (EXTRA_PULMONARY_LOC, TB_DRUGS_FREQ, TB_TYPE,
                       YES_NO_UNK_PNTA, TB_THERAPY_REASONS, TB_PRESCRIPTION_AGE)

from .child_crf_model_mixin import ChildCrfModelMixin


class TbHistoryAdol(ChildCrfModelMixin):
    prior_tb_infec = models.CharField(
        verbose_name='Do you have a prior history of TB infection?',
        choices=YES_NO_UNK_PNTA,
        max_length=30,
        help_text=('TB infection, known as latent TB, is defined as persons '
                   'who are infected by the bacterium, M. tuberculosis, but '
                   'have no TB symptoms. TB infection is diagnosed with a positive '
                   'tuberculin skin test (TST) or IGRA lab test. '))

    history_of_tbt = models.CharField(
        verbose_name=('Do you have a prior history of taking TB '
                      'preventative therapy (TPT)?'),
        choices=YES_NO_UNK_PNTA,
        help_text='This is generally a medication taken for several '
        'months to prevent TB disease, such as isoniazid.',
        max_length=30)
    
    reason_for_therapy = models.CharField(
        verbose_name='What was the reason for taking TB preventative therapy (TPT)?',
        choices=TB_THERAPY_REASONS,
        max_length=12,
        blank=True,
        null=True,
    )
    
    reason_for_therapy_other = OtherCharField()
    
    
    therapy_prescribed_age = models.CharField(
        verbose_name='How old were you when you were prescribed TB preventative therapy (TPT)?',
        choices=TB_PRESCRIPTION_AGE,
        max_length=10,
        blank=True,
        null=True,
    )
    

    tbt_completed = models.CharField(
        verbose_name='Did you complete your TB preventative therapy (TPT)?',
        choices=YES_NO_UNK_PNTA,
        max_length=30,
        blank=True,
        null=True)

    prior_tb_history = models.CharField(
        verbose_name='Do you have a prior history of TB disease?',
        choices=YES_NO_UNK_PNTA,
        max_length=30,
        help_text=('TB disease, known as active TB, is defined as persons who '
                   'are infected by the bacterium, M. tuberculosis, with TB '
                   'symptoms or positive laboratory findings, such as Gene Xpert '
                   'or sputum culture.'))

    tb_diagnosis_type = models.CharField(
        verbose_name='What type of TB were you diagnosed with?',
        choices=TB_TYPE,
        max_length=30,
        blank=True,
        null=True,
        help_text=("TB can occur in the lungs, outside the lungs (ex: lymph nodes, abdomen, bones, brain), or both inside and outside the lungs"))

    extra_pulmonary_loc = models.CharField(
        verbose_name='Where was the location of your TB?',
        choices=EXTRA_PULMONARY_LOC,
        max_length=40,
        blank=True,
        null=True)

    other_loc = models.TextField(
        verbose_name="If other, specify: (free text)",
        blank=True,
        null=True)

    prior_treatmnt_history = models.CharField(
        verbose_name='Do you have a prior history of taking TB treatment?',
        choices=YES_NO_UNK_PNTA,
        max_length=30,
        help_text='TB treatment generally requires 4 drugs for 6 months or longer.',
        null=True,
        blank=True)

    tb_drugs_freq = models.CharField(
        verbose_name='How many drugs did you take for TB treatment?',
        choices=TB_DRUGS_FREQ,
        max_length=30,
        blank=True,
        null=True)

    iv_meds_used = models.CharField(
        verbose_name='Did you take any intravenous (IV) medications during TB treatment?',
        choices=YES_NO_UNK_PNTA,
        max_length=30,
        blank=True,
        null=True)

    tb_treatmnt_completed = models.CharField(
        verbose_name='Did you complete TB treatment? ',
        choices=YES_NO_UNK_PNTA,
        max_length=30,
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB History'
        verbose_name_plural = 'TB History'
