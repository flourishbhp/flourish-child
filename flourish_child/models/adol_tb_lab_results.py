
from django.db import models

from ..choices import POS_NEG_IND_INVALID
from .child_crf_model_mixin import ChildCrfModelMixin


class TbLabResultsAdol(ChildCrfModelMixin):
    quantiferon_result = models.CharField(
        verbose_name='Quentiferon test results',
        choices=POS_NEG_IND_INVALID, max_length=8)
    
    quantiferon_date = models.DateField(
        verbose_name='Quentiferon test date'
    )
    
    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Lab Result'
        verbose_name_plural = "Lab Result"

