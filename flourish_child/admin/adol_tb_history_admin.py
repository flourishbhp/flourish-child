from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import TbHistoryAdolForm
from ..models import TbHistoryAdol
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(TbHistoryAdol, site=flourish_child_admin)
class TbHistoryAdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = TbHistoryAdolForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'prior_tb_infec',
                'history_of_tbt',
                'reason_for_therapy',
                'therapy_prescribed_age',
                'tbt_completed',
                'prior_tb_history',
                'tb_diagnosis_type',
                'extra_pulmonary_loc',
                'prior_treatmnt_history',
                'tb_drugs_freq',
                'iv_meds_used',
                'tb_treatmnt_completed'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'prior_tb_infec': admin.VERTICAL,
                    'history_of_tbt': admin.VERTICAL,
                    'tbt_completed': admin.VERTICAL,
                    'prior_tb_history': admin.VERTICAL,
                    'tb_diagnosis_type': admin.VERTICAL,
                    'extra_pulmonary_loc': admin.VERTICAL,
                    'prior_treatmnt_history': admin.VERTICAL,
                    'tb_drugs_freq': admin.VERTICAL,
                    'iv_meds_used': admin.VERTICAL,
                    'tb_treatmnt_completed': admin.VERTICAL,
                    'reason_for_therapy': admin.VERTICAL,
                    'therapy_prescribed_age': admin.VERTICAL}
