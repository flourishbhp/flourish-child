from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from edc_base.sites.admin import ModelAdminSiteMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildDatasetForm
from ..models import ChildDataset


@admin.register(ChildDataset, site=flourish_child_admin)
class ChildDatasetAdmin(ModelAdminSiteMixin, admin.ModelAdmin):

    form = ChildDatasetForm

    fieldsets = (
        (None, {
            'fields': [
                'study_child_identifier',
                'study_maternal_identifier',
                'subject_identifier',
                'first_name',
                'last_name',
                'dob',
                'infant_enrolldate',
                'infant_randdt',
                'infant_sex',
                'infant_azt_birth',
                'infant_azt_days',
                'infant_azt_startdate',
                'infant_azt_stopdate',
                'infant_sdnvp_birth',
                'infant_hiv_exposed',
                'infant_hiv_status',
                'infant_breastfed',
                'infant_breastfed_days',
                'weaned',
                'weandt',
                'weancat',
                'birthweight',
                'birthwtcat',
                'height_0',
                'headcirc_0',
                'apgarscore_1min',
                'apgarscore_5min',
                'apgarscore_10min',
                'low_birthweight',
                'infant_premature',
                'height_6mo',
                'height_18mo',
                'height_24mo',
                'headcirc_18mo',
                'headcirc_24mo',
                'weight_18mo',
                'weight_24mo',
                'infant_vitalstatus_final',
                'deathdt',
                'deathcause',
                'firsthospdt',
                'hospnum',
                'idth',
                'idth_days',
                'ihiv',
                'ihiv_days',
                'ihosp',
                'ihosp_days',
                'infantvacc_bcg',
                'infantvacc_dtap',
                'infantvacc_hbv',
                'infantvacc_hiv',
                'infantvacc_measles',
                'infantvacc_mmr',
                'infantvacc_pneum',
                'infantvacc_polio',
                'infantvacc_rota',
                'infant_offstudydate',
                'infant_lastcontactdt',
                'infant_onstudy_days',
                'infant_offstudy_reason',
                'curr_age',
                'age_gt17_5',
                'infant_offstudy_complete',
                # 'today',
                'offstrs',
                'offstcd',
            ]}
         ), audit_fieldset_tuple)

    list_display = ('study_child_identifier',
                    'subject_identifier',
                    'infant_enrolldate',
                    'infant_sex',
                    'infant_hiv_exposed',
                    'infant_hiv_status',
                    'infant_offstudydate',
                    'infant_offstudy_reason')

    search_fields = ['subject_identifier', 'study_child_identifier']

    def has_delete_permission(self, request, obj=None):
        return False
