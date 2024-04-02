from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildSafiStigma
from flourish_child_validations.form_validators import ChildSafiStigmaFormValidator


class ChildSafiStigmaForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildSafiStigmaFormValidator

    class Meta:
        model = ChildSafiStigma
        fields = '__all__'
