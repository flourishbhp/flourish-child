from django.contrib import admin
from django.db.models import Q
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

    @property
    def quarterly_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            Q(schedule_type__icontains='quarterly') | Q(schedule_name__icontains='_fu_'),
            onschedule_model__startswith='flourish_child').values_list(
                'schedule_name', flat=True)
        return schedules

    @property
    def conditional_fieldlists(self):
        conditional_fieldlists = {}
        for schedule in self.quarterly_schedules:
            conditional_fieldlists.update(
                {schedule: Insert('socio_demo_changed', after='report_datetime')})
        return conditional_fieldlists

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
