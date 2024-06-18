from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import InfantHIVTesting18MonthsForm, InfantHIVTesting9MonthsForm, \
    InfantHIVTestingAfterBreastfeedingForm, \
    InfantHIVTestingAge6To8WeeksForm, InfantHIVTestingBirthForm, InfantHIVTestingForm, \
    InfantHIVTestingOtherForm
from ..helper_classes.utils import child_utils
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
                'reason_child_not_tested',
                'reason_child_not_tested_other',
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
    }

    search_fields = ('subject_identifier',)

    filter_horizontal = ('reason_child_not_tested', 'test_visit')


class InfantHIVTestingAdminMixin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'child_visit',
                'report_datetime',
                'child_tested_for_hiv',
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

    def get_previous_appt_instance(self, appointment):
        try:
            appointment = appointment.__class__.objects.filter(
                subject_identifier=appointment.subject_identifier,
                visit_schedule_name=appointment.visit_schedule_name,
                schedule_name__endswith=appointment.schedule_name[-11:],
                timepoint_datetime__lte=appointment.timepoint_datetime,
                visit_code_sequence=appointment.visit_code_sequence - 1).latest(
                'timepoint_datetime')
        except appointment.__class__.DoesNotExist:
            return child_utils.get_previous_appt_instance(appointment)
        else:
            return appointment

    def get_previous_instance(self, request, instance=None, **kwargs):
        """Returns a model instance that is the first occurrence of a previous
        instance relative to this object's appointment.
        """
        obj = None
        appointment = instance or self.get_instance(request)

        if appointment:
            while appointment:
                options = {
                    '{}__appointment'.format(self.model.visit_model_attr()):
                        self.get_previous_appt_instance(appointment)}
                try:
                    obj = self.model.objects.get(**options)
                except ObjectDoesNotExist:
                    pass
                else:
                    break
                appointment = self.get_previous_appt_instance(appointment)
        return obj

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form


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
    form = InfantHIVTestingOtherForm

    fieldsets = (
        (None, {
            "fields": (
                'child_visit',
                'report_datetime',
                'child_tested_for_hiv',
                'child_test_date_estimated',
                'test_location',
                'test_location_other',
                'results_received',
                'recall_result_date',
                'received_date',
                'result_date_estimated',
                'hiv_test_result',
                'child_age',
                'additional_comments',
            ),
        }),
        audit_fieldset_tuple,
    )
