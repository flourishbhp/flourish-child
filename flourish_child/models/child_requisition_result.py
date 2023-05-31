from django.db import models
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel

from simple_history.models import HistoricalRecords
from edc_senaite_interface.model_mixins import SenaiteResultModelMixin, SenaiteResultValueMixin


class ChildRequisitionResult(SenaiteResultModelMixin, SiteModelMixin, BaseUuidModel):

    requisition_model = 'flourish_child.childrequisition'

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Child Sample Result'


class ChildResultValue(SenaiteResultValueMixin, BaseUuidModel):

    result = models.ForeignKey(ChildRequisitionResult, on_delete=models.PROTECT)

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Analysis Result Value'
