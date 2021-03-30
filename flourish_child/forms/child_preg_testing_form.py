from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildPregTesting


class ChildPregTestingForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildPregTesting
        fields = '__all__'
