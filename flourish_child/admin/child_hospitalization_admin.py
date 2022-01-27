from django.contrib import admin
from edc_model_admin import StackedInlineMixin

from ..admin_site import flourish_child_admin
from ..forms import ChildHospitalisationForm, AdmissionsReasonsForms
from ..models import ChildHospitalization, AdmissionsReasons
from .model_admin_mixins import ChildCrfModelAdminMixin


class AdmissionsReasonAdmin(StackedInlineMixin,
                            admin.StackedInline):
    model = AdmissionsReasons
    form = AdmissionsReasonsForms
    extra = 0

    radio_fields = {
        'hospital_name': admin.VERTICAL,
        'reason': admin.VERTICAL
    }

    fieldsets = (
        (None, {
            'fields': (
                'hospital_name',
                'hospital_name_other',
                'reason',
                'reason_surgical',
                'reason_other',
                'hosp_date',
            )
        }),
    )


@admin.register(ChildHospitalization, site=flourish_child_admin)
class ChildHospitalizationAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildHospitalisationForm

    radio_fields = {'hospitalized': admin.VERTICAL}

    inlines = [AdmissionsReasonAdmin, ]

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'hospitalized',
                'number_hospitalised',
            )
        }),
    )
