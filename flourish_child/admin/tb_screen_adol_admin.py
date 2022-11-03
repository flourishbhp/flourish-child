from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import TbVisitScreeningAdolescentForm
from ..models import TbVisitScreeningAdolescent


@admin.register(TbVisitScreeningAdolescent, site=flourish_child_admin)
class TbVisitScreeningAdolescentAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = TbVisitScreeningAdolescentForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'have_cough',
                'cough_duration',
                'fever',
                'fever_duration',
                'night_sweats',
                'weight_loss',
                'cough_blood',
                'unexplained_fatigue'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'have_cough': admin.VERTICAL,
                    'have_fever': admin.VERTICAL,
                    'night_sweats': admin.VERTICAL,
                    'weight_loss': admin.VERTICAL,
                    'cough_blood': admin.VERTICAL,
                    'enlarged_lymph': admin.VERTICAL,
                    'unexplained_fatigue': admin.VERTICAL,
                    'tb_screened': admin.VERTICAL}
