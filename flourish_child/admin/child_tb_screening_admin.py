from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import PENDING
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_fieldsets.fieldlist import Insert
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildTBScreeningForm, PreviousFieldsForm
from ..helper_classes.utils import child_utils
from ..models.child_tb_screening import ChildTBScreening


class PreviousResultsAdminMixin(FieldsetsModelAdminMixin, admin.ModelAdmin):

    def get_previous_instances(self, request):
        previous_instances = []
        current_instance = self.get_previous_instance(request)
        while current_instance:
            if self.has_pending_results(current_instance):
                previous_instances.append(current_instance)
            visit = getattr(current_instance, self.visit_attr)
            ap = visit.appointment
            current_instance = self.get_previous_instance(request, ap)
        return previous_instances

    def has_pending_results(self, instance):
        for result in self.update_fields:
            if getattr(instance, result) == PENDING:
                return True
        return False

    def add_view(self, request, form_url='', extra_context=None):
        previous_instances = self.get_previous_instances(request)
        update_fields = self.update_fields
        self.request = request
        if previous_instances:
            extra_context['previous_fields_form'] = PreviousFieldsForm(
                visit_attr=self.visit_attr,
                previous_instances=previous_instances, update_fields=update_fields)

        return self.changeform_view(request, None, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        previous_instances = self.get_previous_instances(request)
        if previous_instances:
            previous_fields_form = PreviousFieldsForm(
                previous_instances=previous_instances,
                update_fields=self.update_fields,
                data=request.POST,
                visit_attr=self.visit_attr,
            )
            if previous_fields_form.is_valid():
                for previous_instance in previous_instances:
                    for result in self.update_fields:
                        visit = getattr(previous_instance, self.visit_attr)
                        field_name = f'{visit.visit_code}_{result}'
                        if field_name in previous_fields_form.cleaned_data:
                            setattr(
                                previous_instance,
                                result,
                                previous_fields_form.cleaned_data[field_name]
                            )
                    previous_instance.save_base(raw=True)
        super().save_model(request, obj, form, change)

    update_fields = [
        'chest_xray_results',
        'sputum_sample_results',
        'stool_sample_results',
        'urine_test_results',
        'skin_test_results',
        'blood_test_results',
    ]


@admin.register(ChildTBScreening, site=flourish_child_admin)
class ChildTBScreeningAdmin(ChildCrfModelAdminMixin, PreviousResultsAdminMixin,
                            admin.ModelAdmin):
    form = ChildTBScreeningForm

    visit_attr = 'child_visit'

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'cough',
                'cough_duration',
                'fever',
                'fever_duration',
                'sweats',
                'sweats_duration',
                'weight_loss',
                'weight_loss_duration',
                'fatigue_or_reduced_playfulness',
                'household_diagnosed_with_tb',
                'evaluated_for_tb',
                'flourish_referral',
                'clinic_visit_date',
                'tb_tests',
                'other_test',
                'chest_xray_results',
                'sputum_sample_results',
                'stool_sample_results',
                'urine_test_results',
                'skin_test_results',
                'blood_test_results',
                'other_test_results',
                'child_diagnosed_with_tb',
                'child_diagnosed_with_tb_other',
                'child_on_tb_treatment',
                'child_on_tb_treatment_other',
                'child_on_tb_preventive_therapy',
                'child_on_tb_preventive_therapy_other',
            ]}),
        audit_fieldset_tuple
    )

    radio_fields = {
        'cough': admin.VERTICAL,
        'cough_duration': admin.VERTICAL,
        'fever': admin.VERTICAL,
        'fever_duration': admin.VERTICAL,
        'sweats': admin.VERTICAL,
        'sweats_duration': admin.VERTICAL,
        'weight_loss': admin.VERTICAL,
        'weight_loss_duration': admin.VERTICAL,
        'fatigue_or_reduced_playfulness': admin.VERTICAL,
        'persistent_symptoms': admin.VERTICAL,
        'household_diagnosed_with_tb': admin.VERTICAL,
        'evaluated_for_tb': admin.VERTICAL,
        'flourish_referral': admin.VERTICAL,
        'chest_xray_results': admin.VERTICAL,
        'sputum_sample_results': admin.VERTICAL,
        'stool_sample_results': admin.VERTICAL,
        'urine_test_results': admin.VERTICAL,
        'skin_test_results': admin.VERTICAL,
        'blood_test_results': admin.VERTICAL,
        'child_diagnosed_with_tb': admin.VERTICAL,
        'child_on_tb_treatment': admin.VERTICAL,
        'child_on_tb_preventive_therapy': admin.VERTICAL,
    }

    filter_horizontal = ('tb_tests',)

    def get_key(self, request, obj=None):
        try:
            model_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            return None
        else:
            return getattr(model_obj, 'schedule_name', None)

    @property
    def quarterly_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            schedule_type__icontains='quarterly',
            onschedule_model__startswith='flourish_child').values_list(
                'schedule_name', flat=True)
        return schedules

    @property
    def conditional_fieldlists(self):
        conditional_fieldlists = {}
        schedules = list(self.quarterly_schedules)

        for schedule in schedules:
            conditional_fieldlists.update(
                {schedule: Insert('persistent_symptoms',
                                  after='fatigue_or_reduced_playfulness')})

        return conditional_fieldlists

