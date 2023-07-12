from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_lab.admin import RequisitionAdminMixin
from edc_lab.admin import requisition_verify_fields
from edc_lab.admin import requisition_verify_fieldset, requisition_status_fieldset
from edc_model_admin import audit_fieldset_tuple, ModelAdminNextUrlRedirectError

from edc_senaite_interface.admin import SenaiteRequisitionAdminMixin

from ..admin_site import flourish_child_admin
from ..forms import ChildRequisitionForm
from ..models import ChildRequisition
from .model_admin_mixins import ChildCrfModelAdminMixin, ExportRequisitionCsvMixin

requisition_identifier_fields = (
    'requisition_identifier',
    'identifier_prefix',
    'primary_aliquot_identifier',
)

requisition_identifier_fieldset = (
    'Identifiers', {
        'classes': ('collapse',),
        'fields': (requisition_identifier_fields)})


@admin.register(ChildRequisition, site=flourish_child_admin)
class ChildRequisitionAdmin(ExportRequisitionCsvMixin, ChildCrfModelAdminMixin,
                            SenaiteRequisitionAdminMixin,
                            RequisitionAdminMixin,
                            admin.ModelAdmin):

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)

        if request.GET.dict().get('next'):
            url_name = settings.DASHBOARD_URL_NAMES.get('child_dashboard_url')
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}

            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')

        return redirect_url

    form = ChildRequisitionForm
    actions = ['export_as_csv']
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
                'exists_on_lis',
                'sample_id',
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
        'exists_on_lis': admin.VERTICAL,
    }

    list_display = ('child_visit', 'is_drawn', 'panel', 'estimated_volume',)

    def get_readonly_fields(self, request, obj=None):
        on_lis = getattr(obj, 'sample_id', None)
        read_only = (super().get_readonly_fields(request, obj)
                     + requisition_identifier_fields
                     + requisition_verify_fields)
        return read_only + ('exists_on_lis', 'sample_id', ) if on_lis else read_only

    def get_previous_instance(self, request, instance=None, **kwargs):
        """Returns a model instance that is the first occurrence of a previous
        instance relative to this object's appointment and panel.
        """
        panel_id = request.GET.get('panel', None)
        obj = None
        appointment = instance or self.get_instance(request)

        if appointment:
            while appointment:
                options = {
                    '{}__appointment'.format(
                        self.model.visit_model_attr()): appointment,
                    'panel__id': panel_id}
                try:
                    obj = self.model.objects.get(**options)
                except self.model.DoesNotExist:
                    pass
                else:
                    break
                appointment = self.get_previous_appt_instance(appointment)
        return obj
