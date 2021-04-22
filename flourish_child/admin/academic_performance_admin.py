from django.apps import apps as django_apps
from django.contrib import admin
from edc_fieldsets.fieldlist import Insert
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
        'num_days': admin.VERTICAL, }

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
                         'science_marks',
                         'setswana_marks',
                         'single_scie_marks',
                         'biology_marks',
                         'chemistry_marks',
                         'physics_marks',
                         'double_scie_marks',
                         after='education_level'),
        }

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
        socio_demographic_obj = self.get_socio_demographic_object(request)

        if socio_demographic_obj:
            education_level = (socio_demographic_obj.education_level
                               or socio_demographic_obj.education_level_other)
            if 'standard' in socio_demographic_obj.education_level:
                return 'primary'
            elif education_level in ['form_1', 'form_2', 'form_3']:
                return 'junior'
            elif education_level in ['form_4', 'form_5']:
                return 'senior'

    def add_view(self, request, form_url='', extra_context=None):
        socio_demographic_obj = self.get_socio_demographic_object(request)

        if socio_demographic_obj is not None:
            g = request.GET.copy()
            g.update({
                'education_level': socio_demographic_obj.get_education_level_display,
            })

            request.GET = g

        return super().add_view(request, form_url, extra_context)
