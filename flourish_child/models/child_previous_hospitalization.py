from django.db import models
from django.core.validators import MinValueValidator

from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from .child_crf_model_mixin import ChildCrfModelMixin
from edc_constants.choices import YES_NO
from ..choices import HOSPITAL
from .list_models import ChildDiseases


class ChildPreviousHospitalization(ChildCrfModelMixin):

    child_hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name='Has your child been hospitalized after birth?')

    hospitalized_count = models.PositiveIntegerField(
        verbose_name='How many times?',
        validators=[MinValueValidator(1)],
        blank=True)

    aprox_date = models.DateField(
        verbose_name='What is the approximate Date of hospitalization?',
        validators=[date_not_future],
        blank=True,
        null=True)

    name_hospital = models.CharField(
        verbose_name='What is the name of the hospital?',
        choices=HOSPITAL,
        max_length=30)

    name_hospital_other = OtherCharField(
        verbose_name='Specify other',
        blank=True,
        null=True,
        max_length=30)

    reason_hospitalized = models.ManyToManyField(
        ChildDiseases,
        verbose_name='What was the reason for hospitalization?',)

    surgical_reason = models.CharField(
        verbose_name='If surgical reason please specify ',
        blank=True,
        null=True,
        max_length=30)

    reason_hospitalized_other = models.CharField(
        verbose_name='Specify other',
        blank=True,
        null=True,
        max_length=30,)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Children/Adolescents Previous Hospital'
        verbose_name_plural = 'Children/Adolescents Previous Hospital'
