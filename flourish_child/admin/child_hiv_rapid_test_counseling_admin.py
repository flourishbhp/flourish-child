from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildHIVRapidTestCounselingForm
from ..models import ChildHIVRapidTestCounseling
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildHIVRapidTestCounseling, site=flourish_child_admin)
class ChildHIVRapidTestCounselingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildHIVRapidTestCounselingForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'rapid_test_done',
                'result_date',
                'result',
                'comments']}
         ), audit_fieldset_tuple)

    list_display = ('child_visit',
                    'rapid_test_done',
                    'result')
    list_filter = ('rapid_test_done', 'result')
    search_fields = ('result_date', )
    radio_fields = {"rapid_test_done": admin.VERTICAL,
                    "result": admin.VERTICAL, }
