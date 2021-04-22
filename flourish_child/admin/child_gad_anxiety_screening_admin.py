from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildGadAnxietyScreeningForm
from ..models import ChildGadAnxietyScreening


@admin.register(ChildGadAnxietyScreening, site=flourish_child_admin)
class ChildGadAnxietyScreeningAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildGadAnxietyScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'feeling_anxious',
                'control_worrying',
                'worrying',
                'trouble_relaxing',
                'restlessness',
                'easily_annoyed',
                'fearful',
                'anxiety_score'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'feeling_anxious': admin.VERTICAL,
                    'control_worrying': admin.VERTICAL,
                    'worrying': admin.VERTICAL,
                    'trouble_relaxing': admin.VERTICAL,
                    'restlessness': admin.VERTICAL,
                    'easily_annoyed': admin.VERTICAL,
                    'fearful': admin.VERTICAL, }

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        return ('anxiety_score', ) + fields
