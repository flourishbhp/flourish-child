from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import TbEngagementForm
from ..models import TbAdolEngagement


@admin.register(TbAdolEngagement, site=flourish_child_admin)
class TbEngagementAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = TbEngagementForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'interview_consent',
                'interview_decline_reason',
                'interview_decline_reason_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'interview_consent': admin.VERTICAL,
        'interview_decline_reason': admin.VERTICAL}
