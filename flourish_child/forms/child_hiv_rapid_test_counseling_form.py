from django import forms

from flourish_child_validations.form_validators import ChildMedicalHistoryFormValidator

from ..models import ChildHIVRapidTestCounseling
from .child_form_mixin import ChildModelFormMixin


class ChildHIVRapidTestCounselingForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildMedicalHistoryFormValidator

    class Meta:
        model = ChildHIVRapidTestCounseling
        fields = '__all__'
