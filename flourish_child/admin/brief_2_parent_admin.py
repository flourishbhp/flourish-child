import json

from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import Brief2ParentForm
from ..models import Brief2Parent


@admin.register(Brief2Parent, site=flourish_child_admin)
class Brief2ParentAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = Brief2ParentForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'memory_retention',
                'lacks_follow_through',
                'task_completion_prob',
                'out_of_control',
                'stronger_reactions',
                'no_planning',
                'poor_writing',
                'action_breaks',
                'unaware_of_others',
                'easily_triggered',
                'trouble_moving_on',
                'stuck_on_activty',
                'caregiver_interest',
                'caregiver_understanding',
                'valid',
                'invalid_reason',
                'other_invalid_reason',
                'impact_on_responses',
                'other_impact_on_responses',
                'overall_comments'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'memory_retention': admin.VERTICAL,
                    'lacks_follow_through': admin.VERTICAL,
                    'task_completion_prob': admin.VERTICAL,
                    'out_of_control': admin.VERTICAL,
                    'stronger_reactions': admin.VERTICAL,
                    'no_planning': admin.VERTICAL,
                    'poor_writing': admin.VERTICAL,
                    'action_breaks': admin.VERTICAL,
                    'unaware_of_others': admin.VERTICAL,
                    'easily_triggered': admin.VERTICAL,
                    'trouble_moving_on': admin.VERTICAL,
                    'stuck_on_activty': admin.VERTICAL,
                    'caregiver_interest': admin.VERTICAL,
                    'caregiver_understanding': admin.VERTICAL,
                    'valid': admin.VERTICAL,
                    'impact_on_responses': admin.VERTICAL,
                    'invalid_reason': admin.VERTICAL, }

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['fields_to_check'] = json.dumps([
            'caregiver_interest',
            'caregiver_understanding',
            'valid',
            'invalid_reason',
            'impact_on_responses',
        ])
        return super().changeform_view(request, object_id, form_url, extra_context)
