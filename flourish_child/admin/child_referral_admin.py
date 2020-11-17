from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ModelAdminMixin

from ..admin_site import flourish_child_admin
from ..forms import ChildReferralForm
from ..models import ChildReferral


@admin.register(ChildReferral, site=flourish_child_admin)
class ChildReferralAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ChildReferralForm

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
