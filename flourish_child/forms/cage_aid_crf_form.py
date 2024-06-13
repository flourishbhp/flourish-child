from django import forms
from .child_form_mixin import ChildModelFormMixin
from ..models import ChildCageAid
from flourish_child_validations.form_validators import ChildCageAidFormValidator


class ChildCageAidForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildCageAidFormValidator

    class Meta:
        model = ChildCageAid
        fields = '__all__'
