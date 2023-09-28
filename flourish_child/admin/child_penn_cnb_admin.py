from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildPennCNBForm
from ..models import ChildPennCNB
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildPennCNB, site=flourish_child_admin)
class ChildPennCNBAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildPennCNBForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'completed',
                'reason_incomplete',
                'reason_other',
                'date_deployed',
                'start_time',
                'stop_time',
                'staff_assisting',
                'testing_impacted',
                'impact_other',
                'claim_experience',
                'laptop_used',
                'comments'
            ]}
         ), audit_fieldset_tuple)

    filter_horizontal = ('staff_assisting', )

    radio_fields = {'completed': admin.VERTICAL,
                    'reason_incomplete': admin.VERTICAL,
                    'testing_impacted': admin.VERTICAL,
                    'laptop_used': admin.VERTICAL,
                    'claim_experience': admin.VERTICAL, }
