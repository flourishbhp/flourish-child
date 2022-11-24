from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import Covid19AdolForm
from ..models import Covid19Adol


@admin.register(Covid19Adol, site=flourish_child_admin)
class Covid19AdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = Covid19AdolForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'test_for_covid',
                'receive_test_result',
                'result_of_test',
            ]}
         ), audit_fieldset_tuple)
    
    radio_fields = {
        'test_for_covid': admin.VERTICAL,
        'receive_test_result': admin.VERTICAL,
        'result_of_test': admin.VERTICAL
    }