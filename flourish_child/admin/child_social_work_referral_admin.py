from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from flourish_child.admin.model_admin_mixins import ChildCrfModelAdminMixin
from flourish_child.forms.child_social_work_referral_form import ChildSocialWorkReferralForm
from flourish_child.models.child_social_work_referral import ChildSocialWorkReferral

from ..admin_site import flourish_child_admin


@admin.register(ChildSocialWorkReferral, site=flourish_child_admin)
class ChildSocialWorkReferralAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildSocialWorkReferralForm

    fieldsets = (
        (None, {
            "fields": (
                'child_visit',
                'report_datetime',
                'referral_for',
                'is_preg',
                'current_hiv_status',
                'child_exposure_status',
                'referral_reason',
                'reason_other',
                'comment',

            ),
        }), audit_fieldset_tuple
    )

    radio_fields = {
        'referral_for': admin.VERTICAL,
        'is_preg': admin.VERTICAL,
        'current_hiv_status': admin.VERTICAL,
        'child_exposure_status': admin.VERTICAL}

    filter_horizontal = ('referral_reason',)
