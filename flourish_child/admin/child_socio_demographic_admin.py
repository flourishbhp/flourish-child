from django.contrib import admin
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
    list_filter = ('ethnicity', )

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
                'house_type',
                'older_than18']}
         ), audit_fieldset_tuple)

    radio_fields = {'ethnicity': admin.VERTICAL,
                    'stay_with_caregiver': admin.VERTICAL,
                    'water_source': admin.VERTICAL,
                    'house_electrified': admin.VERTICAL,
                    'house_fridge': admin.VERTICAL,
                    'cooking_method': admin.VERTICAL,
                    'toilet_facility': admin.VERTICAL,
                    'house_type': admin.VERTICAL}
