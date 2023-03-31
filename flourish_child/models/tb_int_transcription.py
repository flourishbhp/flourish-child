from django.core.validators import FileExtensionValidator
from django.db import models
from edc_base.model_validators import date_not_future

from flourish_child.models.child_crf_model_mixin import ChildCrfModelMixin
from flourish_child.models.model_mixins.intv_users_mixin import IntvUsersMixin


class TbAdolInterviewTranscription(ChildCrfModelMixin, IntvUsersMixin):
    transcription_date = models.DateField(
        verbose_name='Date transcription completed',
        validators=[date_not_future, ], )

    transcriber_name = models.CharField(
        verbose_name='Name of staff who performed transcription',
        max_length=30)

    interview_transcription = models.FileField(
        upload_to='tb_int/docs/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'TB Transcription'
