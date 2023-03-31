from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import InfantArvExposureForm
from ..models import InfantArvExposure
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(InfantArvExposure, site=flourish_child_admin)
class InfantArvExposureAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = InfantArvExposureForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'azt_after_birth',
                'azt_dose_date',
                'azt_additional_dose',
                'sdnvp_after_birth',
                'nvp_dose_date',
                'azt_discharge_supply',
                'infant_arv_comments', ]}
         ), audit_fieldset_tuple)

    list_display = (
        'child_visit', 'azt_after_birth',
        'azt_dose_date', 'azt_additional_dose',
        'sdnvp_after_birth',)

    list_filter = ('azt_after_birth', 'azt_dose_date',
                   'azt_additional_dose', 'sdnvp_after_birth',)

    radio_fields = {
        'azt_after_birth': admin.VERTICAL,
        'azt_additional_dose': admin.VERTICAL,
        'sdnvp_after_birth': admin.VERTICAL,
        'azt_discharge_supply': admin.VERTICAL,
    }
