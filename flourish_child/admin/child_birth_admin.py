from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildBirthForm
from ..models import ChildBirth
from .model_admin_mixins import ModelAdminMixin


@admin.register(ChildBirth, site=flourish_child_admin)
class ChildBirthAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ChildBirthForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'first_name',
                'last_name',
                'initials',
                'dob',
                'gender']}
         ), audit_fieldset_tuple)

    list_display = (
        'report_datetime',
        'first_name',
        'initials',
        'dob',
        'gender',
    )

    search_fields = ['infant_visit__subject_identifier', ]

    list_display = ('report_datetime', 'first_name')
    list_filter = ('gender',)
    radio_fields = {'gender': admin.VERTICAL}
