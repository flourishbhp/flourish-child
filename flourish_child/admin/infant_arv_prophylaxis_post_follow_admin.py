from django.contrib import admin

from flourish_child.admin.model_admin_mixins import ChildCrfModelAdminMixin
from flourish_child.admin_site import flourish_child_admin
from flourish_child.forms import InfantArvProphylaxisPostFollowForm
from flourish_child.models import InfantArvProphylaxisPostFollow


@admin.register(InfantArvProphylaxisPostFollow, site=flourish_child_admin)
class InfantArvProphylaxisPostFollowAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantArvProphylaxisPostFollowForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'prophylactic_med_last_visit',
                'reason_no_art',
                'reason_no_art_other',
                'arv_status',
                'arv_status_incomplete_reason',
                'arv_taken',
                'nvp_start_date',
                'nvp_end_date',
                'azt_start_date',
                'azt_end_date',
                'start_date_3tc',
                'stop_date_3tc',
                'ftc_start_date',
                'ftc_end_date',
                'alu_start_date',
                'alu_end_date',
                'trv_start_date',
                'trv_end_date',
                'tdf_start_date',
                'tdf_end_date',
                'abc_start_date',
                'abc_end_date',
                'ral_start_date',
                'ral_end_date',
                'modification_starting_arv',
                'modification_date',
                'modification_reason',
                'modification_reason_other',
                'modification_reason_side_effects',
                'missed_dose',
                'missed_dose_count',
                'reason_missed',
            )
        }),)

    radio_fields = {
        'prophylactic_med_last_visit': admin.VERTICAL,
        'modification_starting_arv': admin.VERTICAL,
        'missed_dose': admin.VERTICAL,
    }
