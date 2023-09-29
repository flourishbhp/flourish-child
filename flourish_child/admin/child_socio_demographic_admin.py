from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildSocioDemographicForm
from ..models import ChildSocioDemographic
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildSocioDemographic, site=flourish_child_admin)
class ChildSocioDemographicAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildSocioDemographicForm

    list_display = ('child_visit',
                    'ethnicity')
    list_filter = ('ethnicity',)

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'ethnicity',
                'ethnicity_other',
                'stay_with_caregiver',
                'water_source',
                'house_electrified',
                'house_fridge',
                'cooking_method',
                'toilet_facility',
                'toilet_facility_other',
                'house_people_number',
                'older_than18',
                'house_type',
                'attend_school',
                'education_level',
                'education_level_other',
                'school_type',
                'months_in_boarding',
                'working']}
         ), audit_fieldset_tuple)

    radio_fields = {'ethnicity': admin.VERTICAL,
                    'stay_with_caregiver': admin.VERTICAL,
                    'water_source': admin.VERTICAL,
                    'house_electrified': admin.VERTICAL,
                    'house_fridge': admin.VERTICAL,
                    'cooking_method': admin.VERTICAL,
                    'toilet_facility': admin.VERTICAL,
                    'house_type': admin.VERTICAL,
                    'attend_school': admin.VERTICAL,
                    'education_level': admin.VERTICAL,
                    'school_type': admin.VERTICAL,
                    'working': admin.VERTICAL,
                    'socio_demo_changed': admin.VERTICAL}

    custom_form_labels = [
        FormLabel(
            field='socio_demo_changed',
            label=('Since the last time you spoke to a FLOURISH study member, has any of your'
                   ' following Socio-demographic information changed'),
            previous_appointment=True)
        ]

    quartely_schedules = ['child_a_quart_schedule1', 'child_a_fu_qt_schedule1',
                          'child_a_sec_qt_schedule1', 'child_b_quart_schedule1',
                          'child_b_fu_qt_schedule1', 'child_b_sec_qt_schedule1',
                          'child_c_quart_schedule1', 'child_c_fu_qt_schedule1',
                          'child_c_sec_qt_schedule1', 'child_a_fu_schedule1',
                          'child_b_fu_schedule1', 'child_c_fu_schedule1']

    conditional_fieldlists = {}
    for schedule in quartely_schedules:
        conditional_fieldlists.update(
            {schedule: Insert('socio_demo_changed', after='report_datetime')})

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
