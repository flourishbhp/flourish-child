from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildClinicalMeasurementsForm
from ..models import ChildClinicalMeasurements


@admin.register(ChildClinicalMeasurements, site=flourish_child_admin)
class ChildClinicalMeasurementsAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildClinicalMeasurementsForm

    list_display = ('child_visit', 'child_weight_kg', 'child_height',
                    'child_systolic_bp', 'child_diastolic_bp', 'child_waist_circ',
                    'child_hip_circ', 'child_skin_folds')

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'child_height',
                'child_weight_kg',
                'child_systolic_bp',
                'child_diastolic_bp',
                'child_waist_circ',
                'child_hip_circ',
                'child_skin_folds'
            ]}
         ), audit_fieldset_tuple)
