from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildPregTestingForm
from ..models import ChildPregTesting


@admin.register(ChildPregTesting, site=flourish_child_admin)
class ChildPregTestingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildPregTestingForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'test_done',
                'test_date',
                'preg_test_result',
                'comments'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'test_done': admin.VERTICAL,
                    'preg_test_result': admin.VERTICAL}
