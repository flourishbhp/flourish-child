from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from .model_admin_mixins import ChildCrfModelAdminMixin

from ..admin_site import flourish_child_admin
from ..forms import ChildGadReferralForm
from ..models import ChildGadReferral


@admin.register(ChildGadReferral, site=flourish_child_admin)
class ChildGadReferralAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildGadReferralForm

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
