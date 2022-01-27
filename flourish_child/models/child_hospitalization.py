from flourish_child.choices import HOSPITAL, HOSPITALISATION_REASON

from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import date_not_future
from edc_constants.choices import YES_NO
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from .child_crf_model_mixin import ChildCrfModelMixin


class ChildHospitalization(ChildCrfModelMixin):
    hospitalized = models.CharField(
        verbose_name=(
            'Has your infant/child/adolescent been '
            'hospitalized since the last FLOURISH Visit?'),
        choices=YES_NO,
        max_length=100,
        null=True,
    )

    number_hospitalised = models.IntegerField(
        verbose_name=(
            'How many time has your infant/child/adolescent'
            ' been hospitalized?'),
        null=True,
        blank=True
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child Hospitalization'
        verbose_name_plural = 'Child Hospitalization'


class AdmissionsReasons(CrfInlineModelMixin, BaseUuidModel):
    hospital_name = models.CharField(
        verbose_name='What is the name of the hospital?',
        choices=HOSPITAL,
        max_length=50,
        null=True,
        blank=True
    )

    child_hospitalisation = models.ForeignKey(
        ChildHospitalization, on_delete=models.CASCADE
    )

    hospital_name_other = OtherCharField()

    reason = models.CharField(
        verbose_name='What was the reason for the Hospitalisation',
        choices=HOSPITALISATION_REASON,
        max_length=35,
        null=True,
        blank=True
    )

    reason_surgical = models.CharField(
        verbose_name='if Surgical reason, specify',
        max_length=35,
        null=True,
        blank=True
    )

    reason_other = OtherCharField()

    date = models.DateField(
        verbose_name='What is the approximate date of hospitalisation?',
        validators=[date_not_future]
    )

    def natural_key(self):
        return (
                   self.hospital_name,) + self.child_hospitalisation.natural_key()

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Admissions Reasons'
        verbose_name_plural = 'Admissions Reasons'
