from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from edc_base.sites.admin import ModelAdminSiteMixin
from ..admin_site import flourish_infant_admin
from ..forms import InfantDatasetForm
from ..models import InfantDataset


@admin.register(InfantDataset, site=flourish_infant_admin)
class InfantDatasetAdmin(ModelAdminSiteMixin, admin.ModelAdmin):

    form = InfantDatasetForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
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
                'deathcause'
            ]}
         ), audit_fieldset_tuple)

    search_fields = ['subject_identifier']
