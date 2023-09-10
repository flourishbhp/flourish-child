from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins.hiv_rapid_test_conseling_model_mixin import \
    HivRapidTestCounselingModelMixin


class ChildHIVRapidTestCounseling(HivRapidTestCounselingModelMixin, ChildCrfModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child HIV Rapid Testing and Counseling'
        verbose_name_plural = 'Child HIV Rapid Testing and Counseling'
