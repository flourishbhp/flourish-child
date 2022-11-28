
from django.db import models


from ..choices import YES_NO_PNTA, YES_NO_DN_PNTA, TIMES_TESTED
from edc_constants.choices import POS_NEG_IND_UNKNOWN
from .list_models import HIVKnowledgeMedium
from .child_crf_model_mixin import ChildCrfModelMixin


class HivTestingAdol(ChildCrfModelMixin):
    test_for_hiv = models.CharField(
        verbose_name='Have you tested for HIV?',
        choices=YES_NO_DN_PNTA,
        max_length=30
    )
    
    times_tested = models.CharField(
        verbose_name='How many times have you tested for HIV?',
        choices=TIMES_TESTED,
        max_length=4
        
    )
    
    last_result = models.CharField(
        verbose_name='What was the result og yout last test?',
        choices=TIMES_TESTED,
        max_length=4
        
    )
    
    referred_for_treatment = models.CharField(
        verbose_name='Since you were diagnosed with HIV, were you referred to clinic for treatment for HIV?',
        choices=YES_NO_DN_PNTA,
        max_length=10
        
    )
    
    initiated_treatment = models.CharField(
        verbose_name='Have you initiated treatment for HIV?',
        choices=YES_NO_DN_PNTA,
        max_length=10,
        
    )
    
    seen_by_healthcare= models.CharField(
        verbose_name=' Since you were diagnosed with HIV, were you seen by a health care worker for evaluation for tuberculosis',
        choices=YES_NO_DN_PNTA,
        max_length=10
    )
    
    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'HIV Testing'
        verbose_name_plural = 'HIV Testing'
