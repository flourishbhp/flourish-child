from django.contrib import admin
from edc_model_admin import StackedInlineMixin

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms.child_hospitalization_form import ChildHospitalisationForm, \
    AdmissionsReasonsForms
from ..models.child_hospitalization import ChildHospitalization, \
    AdmissionsReasons


class AdmissionsReasonAdmin(StackedInlineMixin,
                            admin.StackedInline):
    model = AdmissionsReasons
    form = AdmissionsReasonsForms
    extra = 1

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
                'date',
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
