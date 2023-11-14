from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import (StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                             audit_fieldset_tuple)

from ..admin_site import flourish_child_admin
from ..forms import ChildMedicalHistoryForm, ChildOutpatientVisitForm
from ..models import ChildMedicalHistory, ChildOutpatientVisit
from .model_admin_mixins import ChildCrfModelAdminMixin


class ChildOutpatientVisitInlineAdmin(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                                      admin.StackedInline):
    model = ChildOutpatientVisit
    form = ChildOutpatientVisitForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'op_type',
                'op_type_other',
                'op_caredate',
                'op_symptoms',
                'op_symp_other',
                'op_new_dx',
                'op_new_dx_details',
                'op_meds_prescribed',
                'op_meds_received',
                'op_meds_other',
                'op_symp_resolved',
                'op_resolution_dt')
            }), audit_fieldset_tuple
        )

    radio_fields = {'op_type': admin.VERTICAL,
                    'op_new_dx': admin.VERTICAL,
                    'op_meds_prescribed': admin.VERTICAL,
                    'op_meds_received': admin.VERTICAL,
                    'op_symp_resolved': admin.VERTICAL, }

    filter_horizontal = ('op_symptoms',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form = self.auto_number(formset.form)
        return formset


@admin.register(ChildMedicalHistory, site=flourish_child_admin)
class ChildMedicalHistoryAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildMedicalHistoryForm

    inlines = [ChildOutpatientVisitInlineAdmin, ]

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
                'had_op_visit',
                'op_visit_count'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'chronic_since': admin.VERTICAL,
                    'currently_taking_medications': admin.VERTICAL,
                    'duration_of_medications': admin.VERTICAL,
                    'current_illness': admin.VERTICAL,
                    'seen_at_local_clinic': admin.VERTICAL,
                    'med_history_changed': admin.VERTICAL,
                    'had_op_visit': admin.VERTICAL, }

    filter_horizontal = (
        'child_chronic', 'current_symptoms', 'current_medications')

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
