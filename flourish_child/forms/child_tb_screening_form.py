from django import forms
from django.core.exceptions import ValidationError

from flourish_child.choices import TEST_RESULTS_CHOICES
from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models.child_tb_screening import ChildTBScreening
from flourish_child_validations.form_validators.child_tb_screening_form_validator import \
    ChildTBScreeningFormValidator


class PreviousResultsFormMixin(forms.Form):
    def clean(self):
        clean_data = super().clean()
        keys_before_child_visit = self.get_keys_before(clean_data, )
        for field in keys_before_child_visit:
            field_value = clean_data.get(field)
            if field_value == '':
                raise ValidationError({field: 'This field is required.'})

    def get_keys_before(self, dict):
        key_stop = "child_visit"
        return_list = []
        for key in dict:
            if key == key_stop:
                break
            return_list.append(key)
        return return_list


class ChildTBScreeningForm(PreviousResultsFormMixin, ChildModelFormMixin):
    form_validator_cls = ChildTBScreeningFormValidator
    update_fields = [
        'chest_xray_results',
        'sputum_sample_results',
        'stool_sample_results',
        'urine_test_results',
        'skin_test_results',
        'blood_test_results',
    ]

    def convert_case(self, raw_string):
        words = raw_string.split('_')
        capitalized_words = [word.capitalize() for word in words]
        return ' '.join(capitalized_words)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        previous_instances = self.previous_instances
        for i, instance in enumerate(previous_instances):
            for field in self.update_fields:
                visit_code = instance.child_visit.visit_code
                new_field_name = f"{visit_code}_{field}_previous"
                self.fields[new_field_name] = forms.ChoiceField(
                    choices=TEST_RESULTS_CHOICES,
                    required=False,
                    label=f"{self.convert_case(field)} for visit {visit_code}",
                    widget=forms.RadioSelect)

    class Meta:
        model = ChildTBScreening
        fields = '__all__'
