from django.db import models

from edc_constants.choices import POS_NEG
from .child_crf_model_mixin import ChildCrfModelMixin


class ChildPregTesting(ChildCrfModelMixin):

    preg_test_result = models.CharField(
        verbose_name='What is the result of the pregnancy test?',
        max_length=10,
        choices=POS_NEG)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Enrollment Pregnancy Testing for Female Adolescents'
        verbose_name_plural = 'Enrollment Pregnancy Testing for Female ' \
                              'Adolescents'
