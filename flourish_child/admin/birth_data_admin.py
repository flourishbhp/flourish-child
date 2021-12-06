from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_child_admin
from ..forms import BirthDataForm
from ..models import BirthData
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(BirthData, site=flourish_child_admin)
class BirthDataAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = BirthDataForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'weight_avail',
                'weight_kg',
                'length_avail',
                'infant_length',
                'head_circ_avail',
                'head_circumference',
                'apgar_score',
                'gestational_age',
                'apgar_score_min_1',
                'apgar_score_min_5',
                'apgar_score_min_10',
                'congenital_anomalities',
                'other_birth_info')}
         ), audit_fieldset_tuple)

    radio_fields = {
        'apgar_score': admin.VERTICAL,
        'congenital_anomalities': admin.VERTICAL,
        'weight_avail': admin.VERTICAL,
        'length_avail': admin.VERTICAL,
        'head_circ_avail': admin.VERTICAL}
