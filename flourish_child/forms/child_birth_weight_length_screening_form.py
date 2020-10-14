from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildBirthWeightLengthScreening


class ChildBirthWeightLengthScreeningForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildBirthWeightLengthScreening
        fields = '__all__'
