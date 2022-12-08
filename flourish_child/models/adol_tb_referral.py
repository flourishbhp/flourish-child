from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from django.db import models
from edc_base.model_validators import date_not_future
from edc_protocol.validators import date_not_before_study_start
from edc_base.utils import get_utcnow
from ..choices import LOCATION_REFERRAL


class TbReferalAdol(ChildCrfModelMixin):
    
    report_datetime = models.DateTimeField(
        verbose_name='Report datetime',
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        default=get_utcnow,)


    referral_date = models.DateField(
        verbose_name="Date of referral",
        validators=[
            date_not_before_study_start,
            date_not_future])

    location = models.CharField(
        verbose_name='Location of referral',
        choices=LOCATION_REFERRAL,
        max_length=15
    )
    
    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB Referral'
