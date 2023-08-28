from django.contrib import admin
from edc_model_admin import (audit_fieldset_tuple, StackedInlineMixin,
                             ModelAdminFormAutoNumberMixin)
from ..admin_site import flourish_child_admin
from ..forms import TbRoutineScreenAdolForm, TbHealthVisitAdolForm
from ..models import TbRoutineScreenAdol, TbHealthVisitAdol
from .model_admin_mixins import ChildCrfModelAdminMixin


class TbHealthVisitAdolInline(admin.StackedInline,
                              StackedInlineMixin,
                              ModelAdminFormAutoNumberMixin,):

    model = TbHealthVisitAdol
    form = TbHealthVisitAdolForm
    extra = 0

    fields = ('care_location',
              'care_location_other',
              'visit_reason',
              'visit_reason_other',
              'screening_questions',
              'pos_screen',
              'diagnostic_referral',
              'diagnostic_studies',
              'diagnostic_studies_other',
              'tb_diagnostic',
              'specify_tests')

    radio_fields = {
        'visit_reason': admin.VERTICAL,
        'screening_questions': admin.VERTICAL,
        'pos_screen': admin.VERTICAL,
        'diagnostic_referral': admin.VERTICAL,
        'diagnostic_studies': admin.VERTICAL,
        'tb_diagnostic': admin.VERTICAL,

    }

    filter_horizontal = ('care_location',)

    def get_formset(self, request, *args, **kwargs):
        formset = super().get_formset(request, *args, **kwargs)
        formset.form = self.auto_number(formset.form)
        return formset


@admin.register(TbRoutineScreenAdol, site=flourish_child_admin)
class TbRoutineScreenAdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = TbRoutineScreenAdolForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'tb_health_visits',
            ]}
         ), audit_fieldset_tuple)

    inlines = [TbHealthVisitAdolInline, ]

    radio_fields = {
        'tb_health_visits': admin.VERTICAL,
    }
