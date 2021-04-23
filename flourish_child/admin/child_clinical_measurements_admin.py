from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_model_admin import audit_fieldset_tuple
from edc_fieldsets.fieldlist import Remove

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildClinicalMeasurementsForm
from ..models import ChildClinicalMeasurements


@admin.register(ChildClinicalMeasurements, site=flourish_child_admin)
class ChildClinicalMeasurementsAdmin(ChildCrfModelAdminMixin,
                                     admin.ModelAdmin):
    form = ChildClinicalMeasurementsForm

    list_display = ('child_visit', 'child_weight_kg', 'child_height',
                    'child_systolic_bp', 'child_diastolic_bp',
                    'child_waist_circ',
                    'child_hip_circ')

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'child_weight_kg',
                'child_systolic_bp',
                'child_diastolic_bp',
                'child_height',
                'child_waist_circ',
                'child_hip_circ',
                'skin_folds_triceps',
                'skin_folds_subscapular',
                'skin_folds_suprailiac',
                'child_muac'
            ]}
         ), audit_fieldset_tuple)

    conditional_fieldlists = {}

    def get_key(self, request, obj=None):
        try:
            appt_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            return None
        else:
            return appt_obj.visit_code

    conditional_fieldlists.update(
        {'1000':
         Remove('skin_folds_triceps',
                'skin_folds_subscapular',
                'skin_folds_suprailiac'), })
