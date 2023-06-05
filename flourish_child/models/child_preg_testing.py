from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins.preg_test_model_mixin import PregTestModelMixin


class ChildPregTesting(ChildCrfModelMixin, PregTestModelMixin):

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Pregnancy Testing for Female Adolescents'
        verbose_name_plural = 'Pregnancy Testing for Female Adolescents'
