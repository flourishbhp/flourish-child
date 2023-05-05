from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import INTERVIEW_LANGUAGE, INTERVIEW_LOCATIONS
from edc_constants.choices import YES_NO


class TbAdolInterview(ChildCrfModelMixin):
    interview_location = models.CharField(
        verbose_name='Location of the interview',
        choices=INTERVIEW_LOCATIONS,
        max_length=100)

    interview_location_other = models.TextField(
        verbose_name='If other, specify ',
        max_length=100,
        null=True,
        blank=True)

    caregiver_present = models.CharField(
        verbose_name='Was the caregiver present for the interview? ',
        choices=YES_NO,
        max_length=3,
    )

    interview_duration = models.PositiveIntegerField(
        verbose_name='Duration of interview:',
        validators=[MinValueValidator(10), MaxValueValidator(1440)],
        help_text='Insert number of minutes')

    # # mp3 upload field
    interview_file = models.FileField(
        upload_to='tb_int/',
        validators=[FileExtensionValidator(['mp3'])],
        null=True)

    interview_language = models.CharField(
        verbose_name='In what language was the interview performed? ',
        choices=INTERVIEW_LANGUAGE,
        max_length=10)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB Interview'
