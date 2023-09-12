from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_child.models.pre_flourish_birth_data import PreFlourishBirthData
from flourish_child_validations.form_validators import \
    PreFlourishBirthDataFormValidator


class PreFlourishBirthDataForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PreFlourishBirthDataFormValidator

    class Meta:
        model = PreFlourishBirthData
        fields = '__all__'
