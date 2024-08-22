from django import forms
from django.contrib import admin
from edc_constants.constants import PENDING
from edc_fieldsets import Fieldsets, FieldsetsModelAdminMixin, Insert
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..choices import TEST_RESULTS_CHOICES
from ..forms import ChildTBScreeningForm
from ..helper_classes.utils import child_utils
from ..models.child_tb_screening import ChildTBScreening


class TbFieldsets(Fieldsets):
    def _get_field_position(self, fields, insert_after):
        try:
            position = fields.index(insert_after) + 1
        except ValueError:
            position = 0
        return position


class PreviousResultsAdminMixin(FieldsetsModelAdminMixin, admin.ModelAdmin):

    def get_previous_results_keys(self, request, obj=None, keys=None):
        if keys is None:
            keys = []
        previous_instances = self.get_previous_instances(request)
        for previous_instance in previous_instances:
            if not obj and previous_instance:
                for result in self.update_fields:
                    if getattr(previous_instance, result) == PENDING:
                        keys.append(result)
        return keys

    def get_previous_instances(self, request):
        previous_instances = []
        current_instance = self.get_previous_instance(request)
        while current_instance:
            if self.has_pending_results(current_instance):
                previous_instances.append(current_instance)
            ap = current_instance.child_visit.appointment
            current_instance = self.get_previous_instance(request, ap)
        return previous_instances

    def has_pending_results(self, instance):
        for result in self.update_fields:
            if getattr(instance, result) == PENDING:
                return True
        return False

    def add_view(self, request, form_url='', extra_context=None):
        self.request = request
        return self.changeform_view(request, None, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        previous_instances = self.get_previous_instances(request)
        if previous_instances:
            for previous_instance in previous_instances:
                changed = False
                for field in form.cleaned_data:
                    if field.endswith('_previous'):
                        original_field_name = field[:-9]
                        previous_value = form.cleaned_data[field]
                        if previous_value != getattr(
                                previous_instance, original_field_name):
                            setattr(previous_instance,
                                    original_field_name, previous_value)
                            changed = True
                if changed:
                    previous_instance.save()
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        previous_instances = self.get_previous_instances(request)

        for i, instance in enumerate(previous_instances):
            for field in self.update_fields:
                visit_code = instance.child_visit.visit_code
                new_field_name = f"{visit_code}_{field}_previous"

                form.base_fields[new_field_name] = forms.ChoiceField(
                    choices=TEST_RESULTS_CHOICES,
                    required=False,
                    label=f"{self.convert_case(field)} for visit {visit_code}",
                    widget=forms.RadioSelect)

        return form

    def convert_case(self, raw_string):
        words = raw_string.split('_')
        capitalized_words = [word.capitalize() for word in words]
        return ' '.join(capitalized_words)

    def remove_unused_section(self, fieldsets):
        fieldsets_list = list(fieldsets)

        for index, fieldset in enumerate(fieldsets_list):
            if fieldset[0] == 'Previous Test Results':
                if len(fieldset[1]['fields']) == 0:
                    del fieldsets_list[index]
                    break

        fieldsets = tuple(fieldsets_list)

        return fieldsets

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

    fieldsets = (
        ('Previous Test Results', {
            'fields': []
        }),
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
                'household_diagnosed_with_tb',
                'evaluated_for_tb',
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
        "cough": admin.VERTICAL,
        "cough_duration": admin.VERTICAL,
        "fever": admin.VERTICAL,
        "fever_duration": admin.VERTICAL,
        "sweats": admin.VERTICAL,
        "sweats_duration": admin.VERTICAL,
        "weight_loss": admin.VERTICAL,
        "weight_loss_duration": admin.VERTICAL,
        "fatigue_or_reduced_playfulness": admin.VERTICAL,
        "household_diagnosed_with_tb": admin.VERTICAL,
        "evaluated_for_tb": admin.VERTICAL,
        "chest_xray_results": admin.VERTICAL,
        "sputum_sample_results": admin.VERTICAL,
        "stool_sample_results": admin.VERTICAL,
        "urine_test_results": admin.VERTICAL,
        "skin_test_results": admin.VERTICAL,
        "blood_test_results": admin.VERTICAL,
        "child_diagnosed_with_tb": admin.VERTICAL,
        "child_on_tb_treatment": admin.VERTICAL,
        "child_on_tb_preventive_therapy": admin.VERTICAL,
    }

    filter_horizontal = ('tb_tests',)

    def get_keys(self, request, obj=None):
        keys = []
        try:
            visit_obj = self.visit_model.objects.get(id=request.GET.get('child_visit'))
        except self.visit_model.DoesNotExist:
            pass
        else:
            subject_identifier = visit_obj.subject_identifier
            child_age = child_utils.child_age(subject_identifier,
                                              visit_obj.report_datetime)
            if child_age and child_age < 12:
                keys.append('not_adol')
        return self.get_previous_results_keys(request, obj, keys)

    @property
    def conditional_fieldlists(self):
        conditional_fieldlists = {
            'not_adol': Insert(('fatigue_or_reduced_playfulness',),
                               after='weight_loss_duration'),
        }
        return self.get_previous_results_conditional_fieldlists(conditional_fieldlists)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = self.add_or_remove_fieldsets(request, obj, fieldsets)
        return fieldsets

    def add_or_remove_fieldsets(self, request, obj, fieldsets):
        keys = self.get_keys(request, obj)
        for key in keys:
            fieldset = self.conditional_fieldlists.get(key)
            if fieldset:
                fieldsets = self.add_fieldsets(fieldsets, fieldset)
        return fieldsets
