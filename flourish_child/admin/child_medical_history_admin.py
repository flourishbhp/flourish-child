from django.contrib import admin
from ..admin_site import flourish_child_admin
from ..forms import ChildMedicalHistoryForm
from ..models import ChildMedicalHistory
from .model_admin_mixins import ChildCrfModelAdminMixin
from edc_model_admin import audit_fieldset_tuple


@admin.register(ChildMedicalHistory, site=flourish_child_admin)
class ChildMedicalHistoryAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildMedicalHistoryForm

    list_display = (
        'child_visit', 'chronic_since')
    list_filter = ('chronic_since',)

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'chronic_since',
                'child_chronic',
                'child_chronic_other',
                'who']}
         ), audit_fieldset_tuple)

    radio_fields = {'chronic_since': admin.VERTICAL}

    filter_horizontal = ('child_chronic', 'who',)
