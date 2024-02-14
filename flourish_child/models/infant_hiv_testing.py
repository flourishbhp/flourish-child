from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins.hiv_testing_and_resulting_mixin import HIVTestingAndResultingMixin
from .model_mixins.hiv_testing_model_mixin import HivTestingModelMixin
from ..choices import YES_NO_DONT_KNOW


class InfantHIVTesting(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant HIV Testing and Results CRF'
        verbose_name_plural = 'Infant HIV Testing and Results CRFs'


class InfantHIVTestingAfterBreastfeeding(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.CharField(
        verbose_name='Date of the HIV test at 3 Months after Cessation of Breastfeeding',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = ('HIV Infant Testing and Results, Three Months After Cessation of '
                        'Breastfeeding')
        verbose_name_plural = (
            'HIV Infant Testing and Results, Three Months After Cessation of '
            'Breastfeeding')


class InfantHIVTestingAge6To8Weeks(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.CharField(
        verbose_name='Date of the HIV test at 6 to 8 Weeks',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 6 TO 8 WEEKS OF AGE'
        verbose_name_plural = 'HIV Infant Testing and Results – 6 TO 8 WEEKS OF AGE '


class InfantHIVTesting9Months(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.CharField(
        verbose_name='Date of the HIV test at 9 Months',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 9 MONTHS OF AGE '
        verbose_name_plural = 'HIV Infant Testing and Results – 9 MONTHS OF AGE '


class InfantHIVTesting18Months(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.CharField(
        verbose_name='Date of the HIV test at 18 Months',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 18 MONTHS'
        verbose_name_plural = 'HIV Infant Testing and Results – 18 MONTHS'


class InfantHIVTestingBirth(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.CharField(
        verbose_name='Date of the HIV test at birth',
        choices=YES_NO_DONT_KNOW,
        max_length=20,
        help_text='Not from FLOURISH Birth visit – Rather from local clinic/hospital'
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – BIRTH'
        verbose_name_plural = 'HIV Infant Testing and Results – BIRTH'


class InfantHIVTestingOther(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – OTHER'
        verbose_name_plural = 'HIV Infant Testing and Results – OTHER'
