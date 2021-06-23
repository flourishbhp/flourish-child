from django import forms

from ..models import ChildClinicianNotes, ClinicianNotesImage
from .child_form_mixin import ChildModelFormMixin, InlineChildModelFormMixin


class ChildClinicianNotesForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildClinicianNotes
        fields = '__all__'


class ClinicianNotesImageForm(InlineChildModelFormMixin):

    class Meta:
        model = ClinicianNotesImage
        fields = '__all__'
