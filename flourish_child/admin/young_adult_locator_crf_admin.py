from django.contrib import admin
from django.http import HttpResponseRedirect
from edc_fieldsets import Fieldsets
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import YoungAdultLocatorCrfForm
from ..models import YoungAdultLocatorCrf


@admin.register(YoungAdultLocatorCrf, site=flourish_child_admin)
class YoungAdultLocatorCrfAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = YoungAdultLocatorCrfForm
    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'along_side_caregiver'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'along_side_caregiver': admin.VERTICAL,
    }
