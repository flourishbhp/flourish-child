from django import forms

from flourish_child_validations.form_validators import ChildPregTestingFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import ChildPregTesting


class ChildPregTestingForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildPregTestingFormValidator

    class Meta:
        model = ChildPregTesting
        fields = '__all__'
