from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO
from edc_constants.constants import YES

from ...choices import CLINIC_VISIT, CURRENT_MEDICATIONS, CURRENT_SYMPTOMS, \
    DURATION_MEDICATIONS


class ChildMedicalHistoryMixin(models.Model):
    """A model completed by the user on Medical History for all children."""

    chronic_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name='Does the Child/Adolescent have any chronic conditions?', )

    child_chronic_other = OtherCharField(
        max_length=35,
        verbose_name='If other, specify.',
        blank=True,
        null=True)

    """Quartely phone calls stem question"""
    med_history_changed = models.CharField(
        verbose_name='Has any of your following medical history changed?',
        max_length=20,
        choices=YES_NO,
        default=YES,
        null=True)

    # version 2 questions
    currently_taking_medications = models.CharField(
        verbose_name='Is your child currently taking any medications',
        choices=YES_NO,
        max_length=10,
        default=''
    )

    current_medications_other = OtherCharField(
        verbose_name='If other, specify.',
        max_length=35,
        blank=True,
        null=True)

    duration_of_medications = models.CharField(
        verbose_name='How long has your child been taking these medications',
        choices=DURATION_MEDICATIONS,
        max_length=50,
        null=True,
        blank=True)

    current_illness = models.CharField(
        verbose_name='Does your child have any current illness',
        choices=YES_NO,
        max_length=10,
        default=''
    )

    current_symptoms_other = models.TextField(
        verbose_name='If other, specify.',
        blank=True,
        null=True)

    symptoms_start_date = models.DateField(
        verbose_name='When did the symptoms start',
        validators=[date_not_future],
        blank=True,
        null=True)

    seen_at_local_clinic = models.CharField(
        verbose_name='Has your child been seen at a local clinic or have you been seen '
                     'for consultation at a local clinic because of this illness?',
        choices=CLINIC_VISIT,
        null=True,
        blank=True,
        max_length=50)

    class Meta:
        abstract = True
