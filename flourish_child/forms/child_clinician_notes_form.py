from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from .child_form_mixin import InlineChildModelFormMixin
from ..models import ChildClinicianNotes, ClinicianNotesImage


class ChildClinicianNotesForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    class Meta:
        model = ChildClinicianNotes
        fields = '__all__'


class ClinicianNotesImageForm(InlineChildModelFormMixin):
    class Meta:
        model = ClinicianNotesImage
        fields = '__all__'
