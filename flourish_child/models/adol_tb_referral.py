from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from django.db import models
from edc_base.utils import get_utcnow
from edc_action_item.model_mixins import ActionModelMixin
from ..choices import LOCATION_REFERRAL
from ..action_items import ADOLESCENT_REFERRAL_ACTION

class TbReferalAdol(ChildCrfModelMixin, ActionModelMixin):
    
    action_name = ADOLESCENT_REFERRAL_ACTION
    
    tracking_identifier_prefix = 'TR'
    
    report_datetime = models.DateTimeField(
        verbose_name='Report datetime',
        null=True,
        default=get_utcnow,)


    referral_date = models.DateField(
        verbose_name="Date of referral",)

    location = models.CharField(
        verbose_name='Location of referral',
        choices=LOCATION_REFERRAL,
        max_length=15
    )
    
    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB Referral'
