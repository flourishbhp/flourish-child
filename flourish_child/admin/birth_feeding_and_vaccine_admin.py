from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import BirthVaccinesForm, BirthFeedingVaccineForm
from ..models import BirthFeedingVaccine, BirthVaccines
from .model_admin_mixins import ChildCrfModelAdminMixin


class BirthVaccinesInline(TabularInlineMixin, admin.TabularInline):

    model = BirthVaccines
    form = BirthVaccinesForm
    extra = 0

    fieldsets = (
        ['Birth Vaccines', {
            'fields': (
                'birth_feed_vaccine',
                'vaccination',
                'vaccine_date')},
         ], audit_fieldset_tuple)


@admin.register(BirthFeedingVaccine, site=flourish_child_admin)
class BirthFeedingVaccineAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = BirthFeedingVaccineForm

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'feeding_after_delivery',
                'breastfeed_start_dt',
                'breastfeed_start_est',
                'formulafeed_start_dt',
                'formulafeed_start_est',
                'comments',
            ]
        }),
    )

    list_display = ('feeding_after_delivery',)

    list_filter = ('feeding_after_delivery',)

    inlines = [BirthVaccinesInline]

    radio_fields = {
        'feeding_after_delivery': admin.VERTICAL,
        'breastfeed_start_est': admin.VERTICAL,
        'formulafeed_start_est': admin.VERTICAL,
    }
