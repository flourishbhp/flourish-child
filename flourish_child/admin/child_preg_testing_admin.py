from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
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

    radio_fields = {'experienced_pregnancy': admin.VERTICAL,
                    'menarche': admin.VERTICAL,
                    'menarche_start_est': admin.VERTICAL,
                    'test_done': admin.VERTICAL,
                    'preg_test_result': admin.VERTICAL,
                    'is_lmp_date_estimated': admin.VERTICAL, }

    schedule_names = ['child_a_sec_qt_schedule1',
                      'child_a_quart_schedule1',
                      'child_b_sec_qt_schedule1',
                      'child_b_quart_schedule1',
                      'child_c_sec_qt_schedule1',
                      'child_c_quart_schedule1', ]
        
    @property
    def quarterly_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            schedule_type__icontains='quarterly',
            onschedule_model__startswith='flourish_child').values_list(
                'schedule_name', flat=True)
        return schedules

    @property
    def fu_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            schedule_type__icontains='followup',
            onschedule_model__startswith='flourish_child').exclude(
                schedule_type__icontains='quarterly').values_list(
                'schedule_name', flat=True)
        return schedules

    @property
    def conditional_fieldlists(self):
        conditional_fieldlists = {}
        for schedule in self.quarterly_schedules:
            conditional_fieldlists.update(
                {schedule: Insert(
                    'menarche',
                    'menarche_start_dt',
                    'menarche_start_est',
                    'experienced_pregnancy',
                    'last_menstrual_period',
                    'is_lmp_date_estimated', after='report_datetime')})

        for schedule in self.fu_schedules:
            conditional_fieldlists.update(
                {schedule: Insert(
                    'menarche',
                    'menarche_start_dt',
                    'menarche_start_est',
                    'experienced_pregnancy',
                    'last_menstrual_period',
                    'is_lmp_date_estimated', after='report_datetime')})

        return conditional_fieldlists
        
    def get_key(self, request, obj=None):
        """ Return schedule name for current appointment instance.
        """
        schedule_name = None
   
        try:
            model_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            schedule_name = None
        else:
            schedule_name = getattr(model_obj, 'schedule_name', None)
        return schedule_name

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form
