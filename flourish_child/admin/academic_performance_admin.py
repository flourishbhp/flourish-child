from django.apps import apps as django_apps
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_fieldsets.fieldlist import Insert
from edc_fieldsets.fieldsets import Fieldsets
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import AcademicPerformanceForm
from ..models import AcademicPerformance
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(AcademicPerformance, site=flourish_child_admin)
class AcademicPerformanceAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = AcademicPerformanceForm

    additional_instructions = ('If participant states the level of school is not correct, '
                               'return to Socio-demographic form to update the class level')

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'education_level',
                'overall_performance',
                'grade_points',
                'num_days')}
         ), audit_fieldset_tuple)

    radio_fields = {
        'mathematics_marks': admin.VERTICAL,
        'science_marks': admin.VERTICAL,
        'setswana_marks': admin.VERTICAL,
        'english_marks': admin.VERTICAL,
        'physical_edu_marks': admin.VERTICAL,
        'cultural_stds_marks': admin.VERTICAL,
        'social_stds_marks': admin.VERTICAL,
        'agriculture_marks': admin.VERTICAL,
        'single_scie_marks': admin.VERTICAL,
        'biology_marks': admin.VERTICAL,
        'chemistry_marks': admin.VERTICAL,
        'physics_marks': admin.VERTICAL,
        'double_scie_marks': admin.VERTICAL,
        'overall_performance': admin.VERTICAL,
        'num_days': admin.VERTICAL,
        'academic_perf_changed': admin.VERTICAL}

    conditional_fieldlists = {
        'primary': Insert('mathematics_marks',
                          'science_marks',
                          'setswana_marks',
                          'english_marks',
                          'physical_edu_marks',
                          'cultural_stds_marks',
                          after='education_level'),
        'junior': Insert('mathematics_marks',
                         'science_marks',
                         'setswana_marks',
                         'english_marks',
                         'social_stds_marks',
                         'agriculture_marks',
                         after='education_level'),
        'senior': Insert('mathematics_marks',
                         'setswana_marks',
                         'single_scie_marks',
                         'biology_marks',
                         'chemistry_marks',
                         'physics_marks',
                         'double_scie_marks',
                         after='education_level'),
        }

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after modifications declared in
        "conditional" dictionaries.
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = Fieldsets(fieldsets=fieldsets)
        keys = self.get_keys(request, obj)
        for key in keys:
            fieldset = self.conditional_fieldsets.get(key)
            if fieldset:
                try:
                    fieldset = tuple(fieldset)
                except TypeError:
                    fieldset = (fieldset,)
                for f in fieldset:
                    fieldsets.add_fieldset(fieldset=f)
            fieldlist = self.conditional_fieldlists.get(key)
            if fieldlist:
                try:
                    fieldsets.insert_fields(
                        *fieldlist.insert_fields,
                        insert_after=fieldlist.insert_after,
                        section=fieldlist.section)
                except AttributeError:
                    pass
                try:
                    fieldsets.remove_fields(
                        *fieldlist.remove_fields,
                        section=fieldlist.section)
                except AttributeError:
                    pass
        fieldsets = self.update_fieldset_for_form(
            fieldsets, request)
        fieldsets.move_to_end(self.fieldsets_move_to_end)
        return fieldsets.fieldsets

    custom_form_labels = [
        FormLabel(
            field='academic_perf_changed',
            label=('Since the last scheduled visit in {previous}, has any of your subject '
                   'marks or overall performance in your last examination changed?'),
            previous_appointment=True)
        ]

    quartely_schedules = ['child_a_quart_schedule1', 'child_a_fu_quart_schedule1',
                          'child_a_sec_qt_schedule1', 'child_b_quart_schedule1',
                          'child_b_fu_quart_schedule1', 'child_b_sec_qt_schedule1',
                          'child_c_quart_schedule1', 'child_c_fu_quart_schedule1',
                          'child_c_sec_qt_schedule1', ]

    for schedule in quartely_schedules:
        conditional_fieldlists.update(
            {schedule: Insert('academic_perf_changed', after='report_datetime')})

    def get_socio_demographic_object(self, request):
        socio_demographic_cls = django_apps.get_model('flourish_child.childsociodemographic')

        try:
            visit_obj = self.visit_model.objects.get(id=request.GET.get('child_visit'))
        except self.visit_model.DoesNotExist:
            return None
        else:
            try:
                socio_demographic_obj = socio_demographic_cls.objects.get(
                    child_visit=visit_obj)
            except socio_demographic_cls.DoesNotExist:
                return None
            else:
                return socio_demographic_obj

    def get_key(self, request, obj=None):
        pass

    def get_keys(self, request, obj=None):
        socio_demographic_obj = self.get_socio_demographic_object(request)

        keys = []
        if self.get_previous_instance(request):
            try:
                model_obj = self.get_instance(request)
            except ObjectDoesNotExist:
                pass
            else:
                schedule_name = model_obj.schedule_name
                keys.append(schedule_name)

        if socio_demographic_obj:
            education_level = (socio_demographic_obj.education_level
                               or socio_demographic_obj.education_level_other)

            if 'standard' in socio_demographic_obj.education_level:
                keys.append('primary')
            elif education_level in ['form_1', 'form_2', 'form_3']:
                keys.append('junior')
            elif education_level in ['form_4', 'form_5']:
                keys.append('senior')
        return keys

    def add_view(self, request, form_url='', extra_context=None):
        socio_demographic_obj = self.get_socio_demographic_object(request)

        if socio_demographic_obj is not None:
            g = request.GET.copy()
            g.update({
                'education_level': socio_demographic_obj.get_education_level_display,
            })

            request.GET = g

        return super().add_view(request, form_url, extra_context)

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form

