from django.contrib import admin
from edc_constants.constants import PENDING
from edc_fieldsets import Insert
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildTBScreeningForm
from ..models.child_tb_screening import ChildTBScreening


@admin.register(ChildTBScreening, site=flourish_child_admin)
class ChildTBScreeningAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildTBScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'cough',
                'cough_duration',
                'fever',
                'fever_duration',
                'sweats',
                'sweats_duration',
                'weight_loss',
                'weight_loss_duration',
                'fatigue_or_reduced_playfulness',
                'household_diagnosed_with_tb',
                'evaluated_for_tb',
                'clinic_visit_date',
                'tb_tests',
                'other_test',
                'chest_xray_results',
                'sputum_sample_results',
                'stool_sample_results',
                'urine_test_results',
                'skin_test_results',
                'blood_test_results',
                'other_test_results',
                'child_diagnosed_with_tb',
                'child_on_tb_treatment',
                'child_on_tb_preventive_therapy',
            ]}),
        audit_fieldset_tuple
    )

    radio_fields = {
        "cough": admin.VERTICAL,
        "cough_duration": admin.VERTICAL,
        "fever": admin.VERTICAL,
        "fever_duration": admin.VERTICAL,
        "sweats": admin.VERTICAL,
        "sweats_duration": admin.VERTICAL,
        "weight_loss": admin.VERTICAL,
        "weight_loss_duration": admin.VERTICAL,
        "fatigue_or_reduced_playfulness": admin.VERTICAL,
        "household_diagnosed_with_tb": admin.VERTICAL,
        "evaluated_for_tb": admin.VERTICAL,
        "tb_tests": admin.VERTICAL,
        "chest_xray_results": admin.VERTICAL,
        "sputum_sample_results": admin.VERTICAL,
        "stool_sample_results": admin.VERTICAL,
        "urine_test_results": admin.VERTICAL,
        "skin_test_results": admin.VERTICAL,
        "blood_test_results": admin.VERTICAL,
        "child_diagnosed_with_tb": admin.VERTICAL,
        "child_on_tb_treatment": admin.VERTICAL,
        "child_on_tb_preventive_therapy": admin.VERTICAL,
    }

