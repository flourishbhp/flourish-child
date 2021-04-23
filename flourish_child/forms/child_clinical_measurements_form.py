from django import forms
from flourish_child_validations.form_validators import ChildClinicalMeasurementsFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildClinicalMeasurements


class ChildClinicalMeasurementsForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildClinicalMeasurementsFormValidator

    class Meta:
        model = ChildClinicalMeasurements
        fields = '__all__'
