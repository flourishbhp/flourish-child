from django.contrib import admin
from edc_constants.constants import PENDING
from edc_fieldsets import Fieldsets, Insert
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
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


@admin.register(ChildTBScreening, site=flourish_child_admin)
class ChildTBScreeningAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
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
            keys.append('not_adol')

        previous_instance = self.get_previous_instance(request)

        if not obj and previous_instance:
            for result in self.update_fields:
                if getattr(previous_instance, result) == PENDING:
                    keys.append(result)

        return keys

    @property
    def conditional_fieldlists(self):
        conditional_fieldlists = {
            'not_adol': Insert(('fatigue_or_reduced_playfulness',),
                               after='weight_loss_duration'),
        }
        for update_field in self.update_fields:
            field = f'{update_field}_previous'
            fieldset = Insert((field,),
                              section='Previous Test Results')
            conditional_fieldlists[update_field] = fieldset
        return conditional_fieldlists

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after modifications declared in
        "conditional" dictionaries.
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = TbFieldsets(fieldsets=fieldsets)
        keys = self.get_keys(request, obj)

        for key in keys:
            fieldlist = self.conditional_fieldlists.get(key)
            if fieldlist:
                try:
                    fieldsets.insert_fields(
                        *fieldlist.insert_fields,
                        insert_after=fieldlist.insert_after,
                        section=fieldlist.section)
                except AttributeError:
                    pass
        self.remove_unused_section(fieldsets=fieldsets)
        fieldsets = self.update_fieldset_for_form(
            fieldsets, request)
        fieldsets.move_to_end(self.fieldsets_move_to_end)
        return fieldsets.fieldsets

    def save_model(self, request, obj, form, change):
        previous_instance = self.get_previous_instance(request)
        if previous_instance:
            changed = False
            for field in form.cleaned_data:
                if field.endswith('_previous'):
                    original_field_name = field[:-9]
                    previous_value = form.cleaned_data[field]
                    if previous_value != getattr(previous_instance, original_field_name):
                        setattr(previous_instance, original_field_name, previous_value)
                        changed = True
            if changed:
                previous_instance.save()
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.previous_instance = self.get_previous_instance(request)
        return form

    def remove_unused_section(self, fieldsets):
        if not fieldsets.fieldsets_asdict['Previous Test Results']['fields']:
            del fieldsets.fieldsets_asdict['Previous Test Results']

    update_fields = [
        'chest_xray_results',
        'sputum_sample_results',
        'stool_sample_results',
        'urine_test_results',
        'skin_test_results',
        'blood_test_results',
    ]
