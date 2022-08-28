from django.contrib import admin
from edc_lab.admin import RequisitionAdminMixin
from edc_lab.admin import requisition_verify_fields
from edc_lab.admin import requisition_verify_fieldset, requisition_status_fieldset
from edc_model_admin import audit_fieldset_tuple
# from edc_senaite_interface.admin import SenaiteRequisitionAdminMixin

from ..admin_site import flourish_child_admin
from ..forms import ChildRequisitionForm
from ..models import ChildRequisition
from .model_admin_mixins import ChildCrfModelAdminMixin, ExportRequisitionCsvMixin

requisition_identifier_fields = (
    'requisition_identifier',
    'identifier_prefix',
    'primary_aliquot_identifier',
    'sample_id',
)

requisition_identifier_fieldset = (
    'Identifiers', {
        'classes': ('collapse',),
        'fields': (requisition_identifier_fields)})


@admin.register(ChildRequisition, site=flourish_child_admin)
class ChildRequisitionAdmin(ExportRequisitionCsvMixin, ChildCrfModelAdminMixin,
                            # SenaiteRequisitionAdminMixin,
                            RequisitionAdminMixin,
                            admin.ModelAdmin):

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
