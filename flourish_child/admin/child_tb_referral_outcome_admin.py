from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_child.admin.model_admin_mixins import ChildCrfModelAdminMixin
from flourish_child.admin_site import flourish_child_admin
from flourish_child.forms.child_tb_referral_outcome_form import ChildTBReferralOutcomeForm
from flourish_child.models import ChildTBReferralOutcome


@admin.register(ChildTBReferralOutcome, site=flourish_child_admin)
class ChildTBReferralOutcomeAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildTBReferralOutcomeForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'tb_evaluation',
                'clinic_name',
                'clinic_name_other',
                'tests_performed',
                'other_test_specify',
                'chest_xray_results',
                'stool_sample_results',
                'sputum_sample_results',
                'urine_test_results',
                'skin_test_results',
                'blood_test_results',
                'other_test_results',
                'diagnosed_with_tb',
                'tb_treatment',
                'other_tb_treatment',
                'tb_preventative_therapy',
                'other_tb_preventative_therapy',
                'tb_isoniazid_preventative_therapy',
                'other_tb_isoniazid_preventative_therapy',
                'reasons',
                'other_reasons',
            ]}
         ), audit_fieldset_tuple)

    filter_horizontal = ('tests_performed',)

    radio_fields = {'tb_evaluation': admin.VERTICAL,
                    'clinic_name': admin.VERTICAL,
                    'chest_xray_results': admin.VERTICAL,
                    'stool_sample_results': admin.VERTICAL,
                    'sputum_sample_results': admin.VERTICAL,
                    'urine_test_results': admin.VERTICAL,
                    'skin_test_results': admin.VERTICAL,
                    'blood_test_results': admin.VERTICAL,
                    'other_test_results': admin.VERTICAL,
                    'diagnosed_with_tb': admin.VERTICAL,
                    'tb_treatment': admin.VERTICAL,
                    'tb_preventative_therapy': admin.VERTICAL,
                    'tb_isoniazid_preventative_therapy': admin.VERTICAL,
                    'reasons': admin.VERTICAL}
