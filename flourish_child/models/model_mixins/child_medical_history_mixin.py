from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO


class ChildMedicalHistoryMixin(models.Model):

    """A model completed by the user on Medical History for all children."""

    chronic_since = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name='Does the Child/Adolescent have any chronic conditions?',)

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
        null=True)

    class Meta:
        abstract = True
