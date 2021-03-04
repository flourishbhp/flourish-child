from django import forms

from flourish_child_validations.form_validators import ChildPreviousHospitalisationFormValidator

from ..models import ChildPreviousHospitalization
from .child_form_mixin import ChildModelFormMixin


class ChildPreviousHospitalizationForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildPreviousHospitalisationFormValidator

    class Meta:
        model = ChildPreviousHospitalization
        fields = '__all__'
