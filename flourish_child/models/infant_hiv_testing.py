from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins.hiv_testing_and_resulting_mixin import HIVTestingAndResultingMixin
from .model_mixins.hiv_testing_model_mixin import HivTestingModelMixin
from ..helper_classes.utils import child_utils


class InfantHIVTesting(ChildCrfModelMixin, HivTestingModelMixin):
    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant HIV Testing and Results CRF'
        verbose_name_plural = 'Infant HIV Testing and Results CRFs'


class InfantHIVTestingAfterBreastfeeding(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.DateField(
        verbose_name='Date of the HIV test at 6 weeks after Cessation of Breastfeeding',
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = ('HIV Infant Testing and Results, 6 Weeks After Cessation of '
                        'Breastfeeding')
        verbose_name_plural = (
            'HIV Infant Testing and Results, 6 Weeks After Cessation of '
            'Breastfeeding')


class InfantHIVTestingAge6To8Weeks(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.DateField(
        verbose_name='Date of the HIV test at 6 to 8 Weeks',
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 6 TO 8 WEEKS OF AGE'
        verbose_name_plural = 'HIV Infant Testing and Results – 6 TO 8 WEEKS OF AGE '


class InfantHIVTesting9Months(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.DateField(
        verbose_name='Date of the HIV test at 9 Months',
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 9 MONTHS OF AGE '
        verbose_name_plural = 'HIV Infant Testing and Results – 9 MONTHS OF AGE '


class InfantHIVTesting18Months(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.DateField(
        verbose_name='Date of the HIV test at 18 Months',
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – 18 MONTHS'
        verbose_name_plural = 'HIV Infant Testing and Results – 18 MONTHS'


class InfantHIVTestingBirth(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.DateField(
        verbose_name='Date of the HIV test at birth',
        help_text='Not from FLOURISH Birth visit – Rather from local clinic/hospital'
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – BIRTH'
        verbose_name_plural = 'HIV Infant Testing and Results – BIRTH'


class InfantHIVTestingOther(ChildCrfModelMixin, HIVTestingAndResultingMixin):
    child_tested_for_hiv = models.DateField(
        verbose_name='Date of the HIV test',
    )

    child_age = models.DecimalField(
        verbose_name='Child age',
        blank=True,
        null=True,
        decimal_places=1,
        max_digits=10
    )

    def save(self, *args, **kwargs):
        if not self.child_age:
            self.child_age = child_utils.child_age(
                subject_identifier=self.subject_identifier,
                report_datetime=self.child_tested_for_hiv)
        super().save(*args, **kwargs)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'HIV Infant Testing and Results – OTHER'
        verbose_name_plural = 'HIV Infant Testing and Results – OTHER'
