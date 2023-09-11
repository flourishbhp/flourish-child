from django.contrib import admin

from flourish_child.admin.model_admin_mixins import ModelAdminMixin
from flourish_child.admin_site import flourish_child_admin
from flourish_child.forms.pre_flourish_birth_data_form import PreFlourishBirthDataForm
from flourish_child.models.pre_flourish_birth_data import PreFlourishBirthData


@admin.register(PreFlourishBirthData, site=flourish_child_admin)
class PreFlourishBirthDataAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = PreFlourishBirthDataForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'dob',
                'place_of_birth',
                'other_place_of_birth',
                'method_of_delivery',
                'gestational_age_known',
                'gestational_age_weeks',
                'gestational_age_months',
                'was_child_born',
                'child_type',
            ]}),
    )

    list_filter = ('subject_identifier', 'report_datetime', 'place_of_birth')

    search_fields = ('subject_identifier', 'report_datetime')

    radio_fields = {
        'place_of_birth': admin.VERTICAL,
        'method_of_delivery': admin.VERTICAL,
        'gestational_age_known': admin.VERTICAL,
        'was_child_born': admin.VERTICAL,
        'child_type': admin.VERTICAL,
    }
