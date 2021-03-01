from django.contrib import admin
from edc_model_admin import TabularInlineMixin, audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import (
    ChildImmunizationHistoryForm, VaccinesReceivedForm, VaccinesMissedForm)
from ..models import ChildImmunizationHistory, VaccinesMissed, VaccinesReceived


class VaccinesReceivedInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = VaccinesReceived
    form = VaccinesReceivedForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'received_vaccine_name',
                'date_given',
                'child_age')
        }), audit_fieldset_tuple
    )


class VaccinesMissedInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = VaccinesMissed
    form = VaccinesMissedForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': (
                'missed_vaccine_name',
                'reason_missed',
                'reason_missed_other')
        }), audit_fieldset_tuple
    )


@admin.register(ChildImmunizationHistory, site=flourish_child_admin)
class ChildImmunizationHistoryAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildImmunizationHistoryForm

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'vaccines_missed',)
        }),
    )

    inlines = [VaccinesReceivedInlineAdmin, VaccinesMissedInlineAdmin, ]
    radio_fields = {'vaccines_missed': admin.VERTICAL}
