from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildPhqDepressionScreeningForm
from ..models import ChildPhqDepressionScreening


@admin.register(ChildPhqDepressionScreening, site=flourish_child_admin)
class ChildPhqDepressionScreeningAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildPhqDepressionScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'depressed',
                'activity_interest',
                'sleep_disorders',
                'eating_disorders',
                'fatigued',
                'self_doubt',
                'easily_distracted',
                'restlessness',
                'self_harm',
                'felt_depressed',
                'problems_effect',
                'self_harm_thoughts',
                'suidice_attempt',
                'depression_score'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'activity_interest': admin.VERTICAL,
                    'depressed': admin.VERTICAL,
                    'sleep_disorders': admin.VERTICAL,
                    'fatigued': admin.VERTICAL,
                    'eating_disorders': admin.VERTICAL,
                    'self_doubt': admin.VERTICAL,
                    'easily_distracted': admin.VERTICAL,
                    'restlessness': admin.VERTICAL,
                    'self_harm': admin.VERTICAL,
                    'felt_depressed': admin.VERTICAL,
                    'problems_effect': admin.VERTICAL,
                    'self_harm_thoughts': admin.VERTICAL,
                    'suidice_attempt': admin.VERTICAL, }

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        return ('depression_score', ) + fields
