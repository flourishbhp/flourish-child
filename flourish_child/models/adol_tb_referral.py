from django.db import models
from edc_base.utils import get_utcnow
from ..choices import LOCATION_REFERRAL, YES_NO_UNK_PNTA, \
    VISIT_NUMBER, HEALTH_CARE_CENTER, YES_NO_DN_PNTA, \
        TB_SYMPTOM, TB_DIAGONISTIC_TYPE, YES_NO_PENDING_UNK 
    
from .child_crf_model_mixin import ChildCrfModelMixin
from .list_models import TbRoutineScreenAdolMedium
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel


class TbReferalAdol(ChildCrfModelMixin):

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
    
    location_other = OtherCharField()

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB Adol. Referral'
