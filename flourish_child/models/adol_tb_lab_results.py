
from django.db import models

from ..choices import POS_NEG_IND
from .child_crf_model_mixin import ChildCrfModelMixin


class TbLabResultsAdol(ChildCrfModelMixin):
    quantiferon_result = models.CharField(choices=POS_NEG_IND, max_length=3)
    
    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Lab Result'
        verbose_name_plural = "Lab Result"

