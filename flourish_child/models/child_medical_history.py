from django.db import models
from django.core.validators import MinValueValidator
from edc_base.model_mixins import BaseUuidModel
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_base.model_validators import date_not_future
from edc_base.model_fields import OtherCharField
from edc_protocol.validators import date_not_before_study_start
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from .list_models import ChronicConditions, GeneralSymptoms, Medications, OutpatientSymptoms
from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins import ChildMedicalHistoryMixin
from ..choices import OP_TYPE, OP_MEDICATIONS


class ChildMedicalHistory(ChildCrfModelMixin,
                          ChildMedicalHistoryMixin):
    """A model completed by the user on Medical History for all children."""

    child_chronic = models.ManyToManyField(
        ChronicConditions,
        related_name='child_chronic_conditions',
        verbose_name=('Does the Child/Adolescent have any of the above. '
                      'Tick all that apply'),
    )

    current_symptoms = models.ManyToManyField(
        GeneralSymptoms,
        verbose_name="What are your child's current symptoms",
        blank=True,
    )

    current_medications = models.ManyToManyField(
        Medications,
        verbose_name='What medications does your child currently take',
        blank=True,
    )

    had_op_visit = models.CharField(
        verbose_name=('Since the last you spoke to FLOURISH staff, '
                      'has your child had an out-patient clinic visit?'),
        choices=YES_NO,
        max_length=3,
        default=NO)

    op_visit_count = models.PositiveIntegerField(
        verbose_name='How many out-patient clinic visits has your child had?',
        validators=[MinValueValidator(1)],
        null=True,
        blank=True)

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Children/Adolescents Medical History'
        verbose_name_plural = 'Children/Adolescents Medical History'


class ChildOutpatientVisit(CrfInlineModelMixin, BaseUuidModel):

    child_medical_history = models.ForeignKey(
        ChildMedicalHistory, on_delete=models.CASCADE)

    op_type = models.CharField(
        verbose_name='What type of care did you seek for your child',
        choices=OP_TYPE,
        max_length=13)

    op_type_other = OtherCharField()

    op_caredate = models.DateField(
        verbose_name=('Approximate date of when you’re child attended '
                      'the out-patient care'),
        validators=[date_not_future, date_not_before_study_start])

    op_symptoms = models.ManyToManyField(
        OutpatientSymptoms,
        related_name='child_op_symptoms',
        verbose_name='What symptoms did your child present with (select all that apply)',
        blank=True)

    op_symp_other = OtherCharField()

    op_new_dx = models.CharField(
        verbose_name='Did you receive a new diagnosis?',
        choices=YES_NO,
        max_length=3)

    op_new_dx_details = models.TextField(
        verbose_name='What was your child’s diagnosis',
        null=True,
        blank=True)

    op_meds_prescribed = models.CharField(
        verbose_name=('Did the healthcare worker prescribe any medications'
                      ' for your child?'),
        choices=YES_NO,
        max_length=3)

    op_meds_received = models.CharField(
        verbose_name='What type of medications did your child receive',
        choices=OP_MEDICATIONS,
        max_length=15,
        null=True,
        blank=True)

    op_meds_other = OtherCharField()

    op_symp_resolved = models.CharField(
        verbose_name='Did your child’s symptoms resolve?',
        choices=YES_NO,
        max_length=3,
        null=True,
        blank=True)

    op_resolution_dt = models.DateField(
        verbose_name='What is the approximate date your child’s symptoms resolve',
        validators=[date_not_future, date_not_before_study_start],
        null=True,
        blank=True)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Child Out-patient Visit'
        verbose_name_plural = 'Child Out-patient Visits'
        unique_together = (
            ('child_medical_history', 'op_caredate'))
