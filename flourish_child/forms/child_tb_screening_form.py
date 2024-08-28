from django import forms
from edc_constants.constants import PENDING

from flourish_child.choices import TEST_RESULTS_CHOICES
from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models.child_tb_screening import ChildTBScreening
from flourish_child_validations.form_validators.child_tb_screening_form_validator import \
    ChildTBScreeningFormValidator


class PreviousFieldsForm(forms.Form):

    def convert_case(self, raw_string):
        words = raw_string.split('_')
        capitalized_words = [word.capitalize() for word in words]
        return ' '.join(capitalized_words)

    def __init__(self, previous_instances=None, update_fields=None, visit_attr=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        if previous_instances:
            for previous_instance in previous_instances:
                visit = getattr(previous_instance, visit_attr)
                visit_code = visit.visit_code
                for result in update_fields:
                    if getattr(previous_instance, result) == PENDING:
                        self.fields[f'{visit_code}_{result}'] = forms.ChoiceField(
                            choices=TEST_RESULTS_CHOICES,
                            required=False,
                            label=f"{self.convert_case(result)} for visit "
                                  f"{visit_code}",
                            widget=forms.RadioSelect,
                            initial=getattr(previous_instance, result)
                        )

        fields_order = list(self.fields.keys())
        self.order_fields(fields_order)


class ChildTBScreeningForm(ChildModelFormMixin):
    form_validator_cls = ChildTBScreeningFormValidator

    class Meta:
        model = ChildTBScreening
        fields = '__all__'
