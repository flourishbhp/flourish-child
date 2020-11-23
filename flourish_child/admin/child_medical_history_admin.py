from django.contrib import admin
from ..admin_site import flourish_child_admin
from ..forms import ChildMedicalHistoryForm
from ..models import ChildMedicalHistory
from .model_admin_mixins import ChildCrfModelAdminMixin
from edc_model_admin import audit_fieldset_tuple


@admin.register(ChildMedicalHistory, site=flourish_child_admin)
class ChildMedicalHistoryAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildMedicalHistoryForm

    list_display = (
        'child_visit', 'chronic_since', 'sero_posetive',
        'date_hiv_diagnosis', 'perinataly_infected',
        'lowest_cd4_known', 'cd4_count', 'cd4_date')
    list_filter = (
        'chronic_since', 'sero_posetive',
        'date_hiv_diagnosis', 'perinataly_infected')

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'chronic_since',
                'who_diagnosis',
                'who',
                'mother_chronic',
                'mother_chronic_other',
                'father_chronic',
                'father_chronic_other',
                'mother_medications',
                'mother_medications_other',
                'sero_posetive',
                'date_hiv_diagnosis',
                'perinataly_infected',
                'know_hiv_status',
                'lowest_cd4_known',
                'cd4_count',
                'cd4_date',
                'is_date_estimated',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'chronic_since': admin.VERTICAL,
                    'who_diagnosis': admin.VERTICAL,
                    'sero_posetive': admin.VERTICAL,
                    'perinataly_infected': admin.VERTICAL,
                    'know_hiv_status': admin.VERTICAL,
                    'lowest_cd4_known': admin.VERTICAL,
                    'is_date_estimated': admin.VERTICAL}
    filter_horizontal = (
        'who', 'mother_chronic', 'father_chronic', 'mother_medications')
