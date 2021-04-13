from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildWorkingStatusForm
from ..models import ChildWorkingStatus
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildWorkingStatus, site=flourish_child_admin)
class ChildWorkingStatusAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildWorkingStatusForm

    list_display = ('child_visit', 'paid', 'work_type', 'work_type_other', )
    list_filter = ('paid', 'work_type', )

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'paid',
                'work_type',
                'work_type_other']}
         ), audit_fieldset_tuple)

    radio_fields = {'paid': admin.VERTICAL,
                    'work_type': admin.VERTICAL}
