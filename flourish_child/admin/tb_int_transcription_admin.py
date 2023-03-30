from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import TbInterviewTranscriptionForm
from ..models import TbAdolInterviewTranscription


@admin.register(TbAdolInterviewTranscription, site=flourish_child_admin)
class TbInterviewTranscriptionAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = TbInterviewTranscriptionForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'transcription_date',
                'transcriber_name',
                'interview_transcription'
            ]}
         ), audit_fieldset_tuple)
