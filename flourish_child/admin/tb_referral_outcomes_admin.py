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
                'reason_not_going',
                'reason_not_going_other',
                'tb_eval_location',
                'tb_eval_location_other',
                'tb_eval_comments',
                'tb_diagnostic_perf',
                'tb_diagnostics',
                'tb_diagnostics_other',
                'tb_diagnostics_other_results',
                'sputum_sample',
                'chest_xray',
                'gene_xpert',
                'tst_or_mentoux',
                'covid_19',
                'tb_treat_start',
                'tb_prev_therapy_start',
                'tb_comments'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'tb_eval': admin.VERTICAL,
        'reason_not_going': admin.VERTICAL,
        'tb_eval_location': admin.VERTICAL,
        'tb_diagnostic_perf': admin.VERTICAL,
        'tb_treat_start': admin.VERTICAL,
        'tb_prev_therapy_start': admin.VERTICAL,
        'sputum_sample': admin.VERTICAL,
        'chest_xray': admin.VERTICAL,
        'gene_xpert': admin.VERTICAL,
        'tst_or_mentoux': admin.VERTICAL,
        'covid_19': admin.VERTICAL, }

    filter_horizontal = ('tb_diagnostics',)
