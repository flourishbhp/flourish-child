from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import InfantHIVTesting18MonthsForm, InfantHIVTesting9MonthsForm, \
    InfantHIVTestingAfterBreastfeedingForm, \
    InfantHIVTestingAge6To8WeeksForm, InfantHIVTestingBirthForm, InfantHIVTestingForm
from ..models import (InfantHIVTesting, InfantHIVTesting18Months,
                      InfantHIVTesting9Months, \
                      InfantHIVTestingAfterBreastfeeding, \
                      InfantHIVTestingAge6To8Weeks, InfantHIVTestingBirth,
                      InfantHIVTestingOther)


@admin.register(InfantHIVTesting, site=flourish_child_admin)
class InfantHIVTestingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = InfantHIVTestingForm

    fieldsets = (
        (None, {
            "fields": (
                'child_visit',
                'report_datetime',
                'child_tested_for_hiv',
                'test_visit',
                'test_visit_other',
                'not_tested_reason',
                'not_tested_reason_other',
                'pref_location',
                'pref_location_other',
                'additional_comments',
            ),
        }),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'pref_location': admin.VERTICAL,
        'child_tested_for_hiv': admin.VERTICAL,
        'test_location': admin.VERTICAL,
    }

    search_fields = ('subject_identifier',)


class InfantHIVTestingAdminMixin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'child_visit',
                'report_datetime',
                'child_test_date',
                'child_test_date_estimated',
                'test_location',
                'test_location_other',
                'results_received',
                'recall_result_date',
                'received_date',
                'result_date_estimated',
                'hiv_test_result',
                'additional_comments',
            ),
        }),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'child_test_date_estimated': admin.VERTICAL,
        'test_location': admin.VERTICAL,
        'results_received': admin.VERTICAL,
        'recall_result_date': admin.VERTICAL,
        'result_date_estimated': admin.VERTICAL,
        'hiv_test_result': admin.VERTICAL,
    }

    search_fields = ('subject_identifier',)


@admin.register(InfantHIVTestingAfterBreastfeeding, site=flourish_child_admin)
class InfantHIVTestingAfterBreastfeedingAdmin(InfantHIVTestingAdminMixin,
                                              admin.ModelAdmin):
    form = InfantHIVTestingAfterBreastfeedingForm


@admin.register(InfantHIVTestingAge6To8Weeks, site=flourish_child_admin)
class InfantHIVTestingAge6To8WeeksAdmin(InfantHIVTestingAdminMixin, admin.ModelAdmin):
    form = InfantHIVTestingAge6To8WeeksForm


@admin.register(InfantHIVTesting9Months, site=flourish_child_admin)
class InfantHIVTesting9MonthsAdmin(InfantHIVTestingAdminMixin, admin.ModelAdmin):
    form = InfantHIVTesting9MonthsForm


@admin.register(InfantHIVTesting18Months, site=flourish_child_admin)
class InfantHIVTesting18MonthsAdmin(InfantHIVTestingAdminMixin, admin.ModelAdmin):
    form = InfantHIVTesting18MonthsForm


@admin.register(InfantHIVTestingBirth, site=flourish_child_admin)
class InfantHIVTestingBirthAdmin(InfantHIVTestingAdminMixin, admin.ModelAdmin):
    form = InfantHIVTestingBirthForm


@admin.register(InfantHIVTestingOther, site=flourish_child_admin)
class InfantHIVTestingOtherAdmin(InfantHIVTestingAdminMixin, admin.ModelAdmin):
    form = InfantHIVTestingForm
