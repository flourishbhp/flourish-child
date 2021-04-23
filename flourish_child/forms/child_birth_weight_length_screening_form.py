from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildBirthScreening


class ChildBirthScreeningForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildBirthScreening
        fields = '__all__'
