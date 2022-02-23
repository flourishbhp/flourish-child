import datetime
import uuid

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from edc_lab.admin import RequisitionAdminMixin
from edc_lab.admin import requisition_identifier_fields
from edc_lab.admin import requisition_identifier_fieldset, requisition_verify_fields
from edc_lab.admin import requisition_verify_fieldset, requisition_status_fieldset
from edc_model_admin import audit_fieldset_tuple
import xlwt

from ..admin_site import flourish_child_admin
from ..forms import ChildRequisitionForm
from ..models import ChildRequisition
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildRequisition, site=flourish_child_admin)
class ChildRequisitionAdmin(ChildCrfModelAdminMixin,
                                RequisitionAdminMixin, admin.ModelAdmin):

    form = ChildRequisitionForm
    actions = ["export_as_csv"]
    ordering = ('requisition_identifier',)

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'requisition_datetime',
                'is_drawn',
                'reason_not_drawn',
                'reason_not_drawn_other',
                'drawn_datetime',
                'study_site',
                'panel',
                'item_type',
                'item_count',
                'estimated_volume',
                'priority',
                'comments',
            )}),
        requisition_status_fieldset,
        requisition_identifier_fieldset,
        requisition_verify_fieldset,
        audit_fieldset_tuple)

    radio_fields = {
        'is_drawn': admin.VERTICAL,
        'reason_not_drawn': admin.VERTICAL,
        'item_type': admin.VERTICAL,
        'priority': admin.VERTICAL,
        'study_site': admin.VERTICAL,
    }

    list_display = ('child_visit', 'is_drawn', 'panel', 'estimated_volume',)

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj)
                +requisition_identifier_fields
                +requisition_verify_fields)
