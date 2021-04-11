from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_child_admin
from ..forms import AcademicPerformanceForm
from ..models import AcademicPerformance
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(AcademicPerformance, site=flourish_child_admin)
class AcademicPerformanceAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = AcademicPerformanceForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'education_level',
                'education_level_other',
                'mathematics_marks',
                'science_marks',
                'setswana_marks',
                'english_marks',
                'physical_edu_marks',
                'cultural_stds_marks',
                'social_stds_marks',
                'agriculture_marks',
                'single_scie_marks',
                'biology_marks',
                'chemistry_marks',
                'physics_marks',
                'double_scie_marks',
                'overall_performance',
                'num_days')}
         ), audit_fieldset_tuple)

    radio_fields = {
        'education_level': admin.VERTICAL,
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
