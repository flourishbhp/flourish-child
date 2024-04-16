from django.db import models
from flourish_caregiver.models.model_mixins import CageAidFieldsMixin
from .child_crf_model_mixin import ChildCrfModelMixin


class ChildCageAid(ChildCrfModelMixin, CageAidFieldsMixin):

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "CAGE-AID Substance Abuse Screening "
        verbose_name_plural = "CAGE-AID Substance Abuse Screening"
