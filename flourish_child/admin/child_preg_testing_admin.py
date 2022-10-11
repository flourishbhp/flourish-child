from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildPregTestingForm
from ..models import ChildPregTesting
from .model_admin_mixins import ChildCrfModelAdminMixin


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

    radio_fields = {'menarche': admin.VERTICAL,
                    'test_done': admin.VERTICAL,
                    'preg_test_result': admin.VERTICAL,
                    'is_lmp_date_estimated': admin.VERTICAL, }

    schedule_names = ['child_a_sec_qt_schedule1',
                      'child_a_quart_schedule1',
                      'child_a_quart_schedule1',
                      'child_a_quart_schedule1',
                      'child_b_sec_qt_schedule1',
                      'child_b_quart_schedule1',
                      'child_c_sec_qt_schedule1',
                      'child_c_quart_schedule1', ]

    conditional_fieldlists = {}

    for schedule in schedule_names:
        conditional_fieldlists.update(
            {schedule: Insert(
                'menarche',
                'last_menstrual_period',
                'is_lmp_date_estimated', after='report_datetime')})

    def get_key(self, request, obj=None):
        return super().get_key(request, obj)
