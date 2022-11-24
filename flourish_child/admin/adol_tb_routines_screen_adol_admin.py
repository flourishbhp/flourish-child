from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import TbRoutineScreenAdolForm
from ..models import TbRoutineScreenAdol
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(TbRoutineScreenAdol, site=flourish_child_admin)
class TbRoutineScreenAdolAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = TbRoutineScreenAdolForm
    
    
    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'tb_health_visits',
                'care_location',
                'care_location_other',
                'visit_reason',
                'visit_reason_other',
                'screening_questions',
                'pos_screen',
                'diagnostic_referral',)}
         ), audit_fieldset_tuple)
    
    
    radio_fields = {
        'tb_health_visits': admin.VERTICAL,
        'visit_reason': admin.VERTICAL,
        'screening_questions': admin.VERTICAL,
        'pos_screen': admin.VERTICAL,
        'diagnostic_referral': admin.VERTICAL
        
    }
    
    filter_horizontal = ('care_location',)
