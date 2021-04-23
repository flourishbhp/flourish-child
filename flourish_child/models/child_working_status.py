from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_constants.choices import YES_NO

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import WORK_TYPE


class ChildWorkingStatus(ChildCrfModelMixin):

    paid = models.CharField(
        verbose_name='Do you get paid at your current job',
        max_length=3,
        choices=YES_NO)

    work_type = models.CharField(
        verbose_name='What type of work do you do?',
        max_length=50,
        choices=WORK_TYPE)

    work_type_other = OtherCharField()

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Working Status for Adolescents'
        verbose_name_plural = 'Working Status for Adolescents'
