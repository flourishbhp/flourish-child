from django import forms
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import FormValidatorMixin as FlourishFormValidatorMixin

from ..models import TbReferalAdol


class TbReferralAdolForm(forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.infant_identifier = self.cleaned_data.get(
            'subject_identifier')
        self.subject_identifier = self.infant_identifier[:-3]
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

    class Meta:
        model = TbReferalAdol
        fields = '__all__'
