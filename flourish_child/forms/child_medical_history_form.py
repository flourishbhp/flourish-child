from django import forms

from flourish_child_validations.form_validators import ChildMedicalHistoryFormValidator

from ..models import ChildMedicalHistory
from .child_form_mixin import ChildModelFormMixin


class ChildMedicalHistoryForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildMedicalHistoryFormValidator

    class Meta:
        model = ChildMedicalHistory
        fields = '__all__'
