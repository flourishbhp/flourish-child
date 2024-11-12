from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms.child_tb_referral_form import ChildTBReferralForm
from ..models.child_tb_referral import ChildTBReferral


@admin.register(ChildTBReferral, site=flourish_child_admin)
class ChildTBReferralAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildTBReferralForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'referred',
                'no_referral_reason',
                'no_referral_reason_other',
                'date_of_referral',
                'reason_for_referral',
                'reason_for_referral_other',
                'clinic_name',
                'clinic_name_other',
                'attend_flourish_clinic'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'clinic_name': admin.VERTICAL,
                    'referred': admin.VERTICAL,
                    'no_referral_reason': admin.VERTICAL,
                    'attend_flourish_clinic': admin.VERTICAL, }
    filter_horizontal = ('reason_for_referral',)
