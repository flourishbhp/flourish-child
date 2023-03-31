from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import TbReferralOutcomesForm
from ..models import TbAdolReferralOutcomes


@admin.register(TbAdolReferralOutcomes, site=flourish_child_admin)
class TbReferralOutcomesAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = TbReferralOutcomesForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'tb_eval',
                'tb_eval_location',
                'tb_eval_location_other',
                'tb_eval_comments',
                'tb_diagnostic_perf',
                'tb_diagnostics',
                'tb_diagnostics_other',
                'tb_diagnose_pos',
                'tb_test_results',
                'tb_treat_start',
                'tb_prev_therapy_start',
                'tb_comments'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'tb_eval': admin.VERTICAL,
        'tb_eval_location': admin.VERTICAL,
        'tb_diagnostic_perf': admin.VERTICAL,
        'tb_diagnose_pos': admin.VERTICAL,
        'tb_treat_start': admin.VERTICAL,
        'tb_prev_therapy_start': admin.VERTICAL, }

    filter_horizontal = ('tb_diagnostics',)
