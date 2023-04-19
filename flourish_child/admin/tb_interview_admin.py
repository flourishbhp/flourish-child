from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import TbInterviewForm
from ..models import TbAdolInterview


@admin.register(TbAdolInterview, site=flourish_child_admin)
class TbInterviewAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = TbInterviewForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'interview_location',
                'interview_location_other',
                'caregiver_present',
                'interview_duration',
                'interview_file',
                'interview_language',

            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'interview_location': admin.VERTICAL,
                    'interview_language': admin.VERTICAL, }
