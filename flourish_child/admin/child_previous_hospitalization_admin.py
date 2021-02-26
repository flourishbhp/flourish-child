from django.contrib import admin


from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildPreviousHospitalizationForm
from ..models import ChildPreviousHospitalization
from edc_model_admin import audit_fieldset_tuple


@admin.register(ChildPreviousHospitalization, site=flourish_child_admin)
class ChildPreviousHospitalizationAdmin(ChildCrfModelAdminMixin,
                                        admin.ModelAdmin):
    form = ChildPreviousHospitalizationForm

    fieldsets = (
        (None, {
            'fields': [
                'child_hospitalized',
                'hospitalized_count',
                'aprox_date',
                'name_hospital',
                'name_hospital_other',
                'reason_hospitalized',
                'surgical_reason',
                'reason_hospitalized_other',

            ]}
         ), audit_fieldset_tuple
    )
    radio_fields = {
        'child_hospitalized': admin.VERTICAL,
        'name_hospital': admin.VERTICAL,
    }

    filter_horizontal = ('reason_hospitalized',)
