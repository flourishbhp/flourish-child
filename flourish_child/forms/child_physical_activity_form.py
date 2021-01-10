from django import forms
from ..models import ChildPhysicalActivity
from .child_form_mixin import ChildModelFormMixin


class ChildPhysicalActivityForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildPhysicalActivity
        fields = '__all__'
