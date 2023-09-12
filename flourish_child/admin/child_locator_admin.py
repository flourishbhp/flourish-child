from django.contrib import admin
from django.http import HttpResponseRedirect
from edc_fieldsets import Fieldsets
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildLocatorForm
from ..models import ChildLocator


@admin.register(ChildLocator, site=flourish_child_admin)
class ChildLocatorAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = ChildLocatorForm
    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'locator_date',
                'first_name',
                'last_name',
                'mail_address',
                'may_visit_home',
                'physical_address',
                'may_call',
                'subject_cell',
                'subject_cell_alt',
                'subject_phone',
                'subject_phone_alt',
                'may_call_work',
                'subject_work_place',
                'subject_work_phone',
                'may_contact_indirectly',
                'indirect_contact_name',
                'indirect_contact_relation',
                'indirect_contact_physical_address',
                'indirect_contact_cell',
                'indirect_contact_phone',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'may_call': admin.VERTICAL,
        'may_call_work': admin.VERTICAL,
        'may_visit_home': admin.VERTICAL,
        'may_contact_indirectly': admin.VERTICAL,
    }

    search_fields = ['subject_identifier', 'study_maternal_identifier']

    list_display = ('subject_identifier', 'may_visit_home',
                    'may_call', 'may_call_work')
