from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin, StackedInlineMixin
from django.core.exceptions import ValidationError
from ..admin_site import flourish_child_admin
from ..forms import TbRoutineScreenAdolForm, TbHealthVisitAdolForm
from ..models import TbRoutineScreenAdol, TbHealthVisitAdol
from .model_admin_mixins import ChildCrfModelAdminMixin


class TbHealthVisitAdolInline(StackedInlineMixin, admin.StackedInline):

    model = TbHealthVisitAdol
    form = TbHealthVisitAdolForm
    extra = 0

    fields = ('care_location',
              'care_location_other',
              'visit_reason',
              'visit_reason_other',
              'screening_questions',
              'pos_screen',
              'diagnostic_referral')
    
    radio_fields = {
        'visit_reason': admin.VERTICAL,
        'screening_questions': admin.VERTICAL,
        'pos_screen': admin.VERTICAL,
        'diagnostic_referral': admin.VERTICAL

    }
    
    filter_horizontal = ('care_location',)


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
         ), )

    inlines = [TbHealthVisitAdolInline, ]

    radio_fields = {
        'tb_health_visits': admin.VERTICAL,
    }
    
    
    
    # def save_formset(self, request, form, formset, change):
        
    #     tb_health_visits = form.cleaned_data.get('tb_health_visits', None)
        
    #     instances = formset.save(commit=False)
        
    #     if tb_health_visits:
            
    #         try:
    #             tb_health_visits_count = int(tb_health_visits)
    #         except ValueError:
    #             formset.save()
    #         else:
    #             if tb_health_visits_count != len(instances):
    #                 # self.message_user(request=request, message='Number of inlines specified is not equal to Q3')
    #                 # raise ValidationError('Number of inlines specified is not equal to Q3')
    #                 # form.
    #                 # formset.save()
    #                 return formset
    #             else:
    #                 return super().save_formset(request, form, formset, change)