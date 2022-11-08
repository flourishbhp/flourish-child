from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import AdolClinicalMeasurementsForm
from ..models import AdolescentClinicalMeasurements


@admin.register(AdolescentClinicalMeasurements, site=flourish_child_admin)
class AdolescentClinicalMeasurementsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = AdolClinicalMeasurementsForm

    list_display = ('child_visit', 'weight_kg', 'systolic_bp',
                    'diastolic_bp')

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'weight_kg',
                'systolic_bp',
                'diastolic_bp',
            ]}
         ), audit_fieldset_tuple)
