from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import NO


class YoungAdultLocatorCrf(ChildCrfModelMixin):
    along_side_caregiver = models.CharField(
        verbose_name='Do you feel comfortable with continuing on the FLOURISH study alongside your caregiver?',
        max_length=3,
        choices=YES_NO,
        default=NO
    )

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Young Adults Locator'
