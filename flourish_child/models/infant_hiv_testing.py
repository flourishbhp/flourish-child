from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins.hiv_testing_model_mixin import HivTestingModelMixin


class InfantHIVTesting(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant HIV Testing and Results CRF'
        verbose_name_plural = 'Infant HIV Testing and Results CRFs'
