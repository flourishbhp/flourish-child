from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins.hiv_testing_model_mixin import HivTestingModelMixin


class InfantHIVTesting(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant HIV Testing and Results CRF'
        verbose_name_plural = 'Infant HIV Testing and Results CRFs'


class InfantHIVTestingAfterBreastfeeding(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = ('HIV Infant Testing and Results, Three Months After Cessation of '
                        'Breastfeeding')
        verbose_name_plural = (
            'HIV Infant Testing and Results, Three Months After Cessation of '
            'Breastfeeding')


class InfantHIVTestingAge6To8Weeks(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 6 TO 8 WEEKS OF AGE'
        verbose_name_plural = 'HIV Infant Testing and Results – 6 TO 8 WEEKS OF AGE '


class InfantHIVTesting9Months(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 9 MONTHS OF AGE '
        verbose_name_plural = 'HIV Infant Testing and Results – 9 MONTHS OF AGE '


class InfantHIVTesting18Months(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 18 MONTHS'
        verbose_name_plural = 'HIV Infant Testing and Results – 18 MONTHS'


class InfantHIVTestingBirth(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – BIRTH'
        verbose_name_plural = 'HIV Infant Testing and Results – BIRTH'


class InfantHIVTestingOther(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – OTHER'
        verbose_name_plural = 'HIV Infant Testing and Results – OTHER'
