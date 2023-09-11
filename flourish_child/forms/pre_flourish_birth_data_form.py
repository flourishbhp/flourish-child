from django import forms

from flourish_child.models.pre_flourish_birth_data import PreFlourishBirthData
from flourish_child_validations.form_validators import \
    PreFlourishBirthDataFormValidator


class PreFlourishBirthDataForm(forms.ModelForm):
    form_validator_cls = PreFlourishBirthDataFormValidator

    class Meta:
        model = PreFlourishBirthData
        fields = '__all__'
