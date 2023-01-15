from django.contrib import admin
from edc_fieldsets.fieldlist import Remove
from edc_model_admin import audit_fieldset_tuple

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
                'is_child_preg',
                'child_weight_kg',
                'child_systolic_bp',
                'child_diastolic_bp',
                'child_height',
                'child_muac'
            ]},
         ),
        ("Child Waist Circumference", {
            'fields': [
                'child_waist_circ',
                'child_waist_circ_second',
                'child_waist_circ_third',
            ]}
         ),
        ("Child Hip Circumference", {
            'fields': [
                'child_hip_circ',
                'child_hip_circ_second',
                'child_hip_circ_third',
            ]}
         ),
        ("Skin Folds Triceps", {
            'fields': [
                'skin_folds_triceps',
                'skin_folds_triceps_second',
                'skin_folds_triceps_third',
            ]}
         ),
        ("Skin Folds Subscapular", {
            'fields': [
                'skin_folds_subscapular',
                'skin_folds_subscapular_second',
                'skin_folds_subscapular_third',
            ]}
         ),
        ("Skin Folds Suprailiac", {
            'fields': [
                'skin_folds_suprailiac',
                'skin_folds_suprailiac_second',
                'skin_folds_suprailiac_third',
            ]}
         ),
        audit_fieldset_tuple)

    radio_fields = {
        'is_child_preg': admin.VERTICAL, }

    conditional_fieldlists = {}

    def get_key(self, request, obj=None):
        if obj:
            return obj.child_visit.visit_code
        else:
            appt_obj = self.get_instance(request)
            return appt_obj.visit_code if appt_obj else None

    conditional_fieldlists.update(
        {'1000':
             Remove('skin_folds_triceps',
                    'skin_folds_triceps_second',
                    'skin_folds_triceps_third',
                    'skin_folds_subscapular',
                    'skin_folds_subscapular_second',
                    'skin_folds_subscapular_third',
                    'skin_folds_suprailiac',
                    'skin_folds_suprailiac_second',
                    'skin_folds_suprailiac_third')})
