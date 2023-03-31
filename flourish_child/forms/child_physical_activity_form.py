from django import forms

from flourish_child_validations.form_validators import ChildPhysicalActivityFormValidator
from ..models import ChildPhysicalActivity
from .child_form_mixin import ChildModelFormMixin


class ChildPhysicalActivityForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildPhysicalActivityFormValidator

    class Meta:
        model = ChildPhysicalActivity
        fields = '__all__'
