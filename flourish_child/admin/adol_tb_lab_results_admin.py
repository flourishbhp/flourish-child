from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import TbLabResultsAdolForm
from ..models import TbLabResultsAdol


@admin.register(TbLabResultsAdol, site=flourish_child_admin)
class TbLabResultAdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = TbLabResultsAdolForm

    list_display = ('child_visit', 'report_datetime', 'quantiferon_result')

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'quantiferon_result',
                'quantiferon_date']}
         ), audit_fieldset_tuple)
    
    radio_fields = {
        'quantiferon_result': admin.VERTICAL
    }
