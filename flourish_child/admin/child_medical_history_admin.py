from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildMedicalHistoryForm
from ..models import ChildMedicalHistory
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildMedicalHistory, site=flourish_child_admin)
class ChildMedicalHistoryAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildMedicalHistoryForm

    list_display = (
        'child_visit', 'chronic_since')
    list_filter = ('chronic_since',)

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'chronic_since',
                'child_chronic',
                'child_chronic_other',
                'current_illness',
                'current_symptoms',
                'current_symptoms_other',
                'symptoms_start_date',
                'seen_at_local_clinic',
                'currently_taking_medications',
                'current_medications',
                'current_medications_other',
                'duration_of_medications',

            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'chronic_since': admin.VERTICAL,
                    'currently_taking_medications': admin.VERTICAL,
                    'current_medications': admin.VERTICAL,
                    'duration_of_medications': admin.VERTICAL,
                    'current_illness': admin.VERTICAL,
                    'current_symptoms': admin.VERTICAL,
                    'seen_at_local_clinic': admin.VERTICAL,
                    'med_history_changed': admin.VERTICAL}

    filter_horizontal = ('child_chronic',)

    custom_form_labels = [
        FormLabel(
            field='med_history_changed',
            label=('Since the last scheduled visit in {previous}, has any of '
                   'your medical history changed?'),
            previous_appointment=True)
    ]

    quartely_schedules = ['child_a_sec_qt_schedule1', 'child_a_quart_schedule1',
                          'child_b_sec_qt_schedule1', 'child_b_quart_schedule1',
                          'child_c_sec_qt_schedule1', 'child_c_quart_schedule1',
                          'child_pool_schedule1', 'child_a_fu_schedule1',
                          'child_b_fu_schedule1', 'child_c_fu_schedule1',
                          'child_a_fu_qt_schedule1', 'child_b_fu_qt_schedule1',
                          'child_c_fu_qt_schedule1']

    conditional_fieldlists = {}
    for schedule in quartely_schedules:
        conditional_fieldlists.update(
            {schedule: Insert('med_history_changed', after='report_datetime')})

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
