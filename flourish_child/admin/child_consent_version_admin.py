from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildConsentVersionForm
from ..models import ChildConsentVersion
from .model_admin_mixins import ModelAdminMixin


@admin.register(ChildConsentVersion, site=flourish_child_admin)
class ChildConsentVersionAdmin(ModelAdminMixin,
                               admin.ModelAdmin):

    form = ChildConsentVersionForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'version',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'version': admin.VERTICAL}

    list_display = ('subject_identifier',
                    'report_datetime',
                    'version', )
