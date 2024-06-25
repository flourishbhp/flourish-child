from django import forms
from django.core.exceptions import ValidationError

from flourish_child.choices import TEST_RESULTS_CHOICES
from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models.child_tb_screening import ChildTBScreening
from flourish_child_validations.form_validators.child_tb_screening_form_validator import \
    ChildTBScreeningFormValidator


class ChildTBScreeningForm(ChildModelFormMixin):
    form_validator_cls = ChildTBScreeningFormValidator

    chest_xray_results_previous = forms.ChoiceField(
        choices=TEST_RESULTS_CHOICES,
        required=False,
        label="Previous Chest X-Ray Results",
        widget=forms.RadioSelect)
    sputum_sample_results_previous = forms.ChoiceField(
        choices=TEST_RESULTS_CHOICES,
        required=False,
        label="Previous Sputum Sample Results",
        widget=forms.RadioSelect)
    stool_sample_results_previous = forms.ChoiceField(
        choices=TEST_RESULTS_CHOICES,
        required=False,
        label="Previous Stool Sample Results",
        widget=forms.RadioSelect)
    urine_test_results_previous = forms.ChoiceField(
        choices=TEST_RESULTS_CHOICES,
        required=False,
        label="Previous Urine Test Results",
        widget=forms.RadioSelect)
    skin_test_results_previous = forms.ChoiceField(
        choices=TEST_RESULTS_CHOICES,
        required=False,
        label="Previous Skin Test Results",
        widget=forms.RadioSelect)
    blood_test_results_previous = forms.ChoiceField(
        choices=TEST_RESULTS_CHOICES,
        required=False,
        label="Previous Blood Test Results",
        widget=forms.RadioSelect)

    def clean(self):
        clean_data = super().clean()
        keys_before_child_visit = self.get_keys_before(clean_data, "child_visit")
        for field in keys_before_child_visit:
            field_value = clean_data.get(field)
            if field_value == '':
                raise ValidationError({field: 'This field is required.'})

    def get_keys_before(self, dict, key_stop):
        return_list = []
        for key in dict:
            if key == key_stop:
                break
            return_list.append(key)
        return return_list

    class Meta:
        model = ChildTBScreening
        fields = '__all__'
