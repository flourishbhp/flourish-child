from django.apps import apps as django_apps
from django.contrib import admin

from edc_fieldsets.fieldlist import Fieldlist
from edc_fieldsets.fieldsets_modeladmin_mixin import FormLabel
from edc_model_admin import TabularInlineMixin, audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import (
    ChildImmunizationHistoryForm, VaccinesReceivedForm, VaccinesMissedForm)
from ..models import ChildImmunizationHistory, VaccinesMissed, VaccinesReceived, BirthFeedingVaccine, ChildVisit
from .model_admin_mixins import ChildCrfModelAdminMixin


class VaccinesReceivedInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = VaccinesReceived
    form = VaccinesReceivedForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'received_vaccine_name',
                'first_dose_dt',
                'second_dose_dt',
                'third_dose_dt',
                'booster_dose_dt',
                'booster_2nd_dose_dt',
                'booster_3rd_dose_dt')
        }),
    )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.request = request
        return formset

    class Media:
        js = ('flourish_child/js/jquery.min.js',
              'flourish_child/js/autocomplete_vaccines.js', )


class VaccinesMissedInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = VaccinesMissed
    form = VaccinesMissedForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'missed_vaccine_name',
                'reason_missed',
                'reason_missed_other')
        }), audit_fieldset_tuple
    )

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


@admin.register(ChildImmunizationHistory, site=flourish_child_admin)
class ChildImmunizationHistoryAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildImmunizationHistoryForm

    extra_context_models = ['vaccinesreceived', 'vaccinesmissed', 'birthvaccines']

    fieldsets = (
        (None, {
            'fields': (
                'child_visit',
                'report_datetime',
                'vaccines_received',
                'vaccines_missed',)
        }),
    )

    inlines = [VaccinesReceivedInlineAdmin, VaccinesMissedInlineAdmin, ]
    radio_fields = {'vaccines_received': admin.VERTICAL,
                    'vaccines_missed': admin.VERTICAL,
                    'rec_add_immunization': admin.VERTICAL}

    custom_form_labels = [
        FormLabel(
            field='rec_add_immunization',
            label=('Since the last scheduled visit in {previous}, have you '
                   'received any additional immunizations?'),
            previous_appointment=True)
    ]

    quartely_schedules = ['child_a_quart_schedule1',
                          'child_a_fu_qt_schedule1',
                          'child_a_sec_qt_schedule1', 'child_b_quart_schedule1',
                          'child_b_fu_qt_schedule1',
                          'child_b_sec_qt_schedule1',
                          'child_c_qt_schedule1',
                          'child_c_fu_quart_schedule1',
                          'child_c_sec_qt_schedule1', 'child_pool_schedule1',
                          'child_a_fu_schedule1',
                          'child_b_fu_schedule1', 'child_c_fu_schedule1']

    conditional_fieldlists = {}

    for schedule in quartely_schedules:
        conditional_fieldlists.update(
            {schedule: Fieldlist(insert_fields=('rec_add_immunization',),
                                 remove_fields=('vaccines_received',),
                                 insert_after='report_datetime')})

    def add_view(self, request, form_url='', extra_context=None):

        extra_context = extra_context or {}
        subject_identifier = request.GET.get('subject_identifier')
        child_visit = request.GET.get('child_visit')
        if self.extra_context_models:
            extra_context = self.get_model_data_per_visit(
                subject_identifier=subject_identifier, child_visit=child_visit)
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        subject_identifier = request.GET.get('subject_identifier')
        child_visit = request.GET.get('child_visit')
        if self.extra_context_models:
            extra_context = self.get_model_data_per_visit(
                subject_identifier=subject_identifier, child_visit=child_visit)
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def get_model_data_per_visit(self, subject_identifier=None,
                                 child_visit=None):
        model_dict = {}
        for model_name in self.extra_context_models:
            data_dict = {}

            if model_name == 'birthvaccines':

                try:
                    birth_feeding_obj = BirthFeedingVaccine.objects.filter(
                        child_visit__subject_identifier=subject_identifier).earliest('report_datetime')

                except BirthFeedingVaccine.DoesNotExist:
                    pass
                else:

                    model_objs = birth_feeding_obj.birthvaccines_set.all()
                    for model_obj in model_objs:
                        visit_code = birth_feeding_obj.visit.visit_code
                        data_dict.setdefault(visit_code, [])
                        data_dict[visit_code].append(model_obj)
                model_dict.update({model_name: data_dict})

            else:

                model_cls = django_apps.get_model(f'flourish_child.{model_name}')
                model_objs = model_cls.objects.filter(
                    child_immunization_history__child_visit__subject_identifier=subject_identifier).exclude(
                    child_immunization_history__child_visit=child_visit)
                for model_obj in model_objs:
                    visit_code = model_obj.visit.visit_code
                    data_dict.setdefault(visit_code, [])
                    data_dict[visit_code].append(model_obj)

                model_dict.update({model_name: data_dict})
        return model_dict
