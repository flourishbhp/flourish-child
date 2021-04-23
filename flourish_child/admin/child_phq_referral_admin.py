from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from .model_admin_mixins import ChildCrfModelAdminMixin

from ..admin_site import flourish_child_admin
from ..forms import ChildPhqReferralForm
from ..models import ChildPhqReferral


@admin.register(ChildPhqReferral, site=flourish_child_admin)
class ChildPhqReferralAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildPhqReferralForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'referred_to',
                'referred_to_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'referred_to': admin.VERTICAL}
