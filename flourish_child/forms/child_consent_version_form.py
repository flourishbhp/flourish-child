from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ChildConsentVersion


class ChildConsentVersionForm(SiteModelFormMixin, FormValidatorMixin,
                              forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ChildConsentVersion
        fields = '__all__'
