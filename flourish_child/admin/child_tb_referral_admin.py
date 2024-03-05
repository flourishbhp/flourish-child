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
                'date_of_referral',
                'reason_for_referral',
                'reason_for_referral_other',
                'clinic_name',
                'clinic_name_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'reason_for_referral': admin.VERTICAL,
                    'clinic_name': admin.VERTICAL, }
