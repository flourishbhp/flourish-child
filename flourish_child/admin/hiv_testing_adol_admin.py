from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import HIVTestingAdolForm
from ..models import HivTestingAdol
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple


@admin.register(HivTestingAdol, site=flourish_child_admin)
class HivTestingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = HIVTestingAdolForm
    
    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'test_for_hiv',
                'times_tested',
                'last_result',
                'referred_for_treatment',
                'initiated_treatment',
                'date_initiated_treatment',
                'seen_by_healthcare',
            ]}),
        audit_fieldset_tuple
    )
    
    radio_fields = {"times_tested": admin.VERTICAL,
                    "last_result": admin.VERTICAL,
                    "referred_for_treatment": admin.VERTICAL,
                    "initiated_treatment": admin.VERTICAL,
                    "seen_by_healthcare": admin.VERTICAL,
                    "test_for_hiv": admin.VERTICAL}

