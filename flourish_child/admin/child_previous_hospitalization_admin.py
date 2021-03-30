from django.contrib import admin


from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildPreviousHospitalizationForm, ChildPreHospitalizationInlineForm
from ..models import ChildPreviousHospitalization, ChildPreHospitalizationInline
from edc_model_admin import StackedInlineMixin
from edc_model_admin import audit_fieldset_tuple


class ChildPreHospitalizationInlineAdmin(StackedInlineMixin, admin.StackedInline):

    model = ChildPreHospitalizationInline
    form = ChildPreHospitalizationInlineForm
    extra = 0

    fieldsets = (
        [None, {
            'fields': (
                'name_hospital',
                'name_hospital_other',
                'reason_hospitalized',
                'surgical_reason',
                'reason_hospitalized_other',
                'aprox_date',)},
         ], audit_fieldset_tuple)

    radio_fields = {
        'name_hospital': admin.VERTICAL,
    }

    filter_horizontal = ['reason_hospitalized']


@admin.register(ChildPreviousHospitalization, site=flourish_child_admin)
class ChildPreviousHospitalizationAdmin(ChildCrfModelAdminMixin,
                                        admin.ModelAdmin):
    form = ChildPreviousHospitalizationForm

    inlines = [ChildPreHospitalizationInlineAdmin, ]

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'child_hospitalized',
                'hospitalized_count',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'child_hospitalized': admin.VERTICAL,
    }
