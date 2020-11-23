from django import forms
from ..models import ChildMedicalHistory
from .child_form_mixin import ChildModelFormMixin


class ChildMedicalHistoryForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildMedicalHistory
        fields = '__all__'
