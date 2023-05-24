from django import forms
from flourish_child_validations.form_validators import InfantHIVTestingFormValidator

from ..models import InfantHIVTesting
from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin


class InfantHIVTestingForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingFormValidator

    class Meta:
        model = InfantHIVTesting
        fields = '__all__'
