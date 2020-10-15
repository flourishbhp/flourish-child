from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildClinicalMeasurements


class ChildClinicalMeasurementsForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildClinicalMeasurements
        fields = '__all__'
