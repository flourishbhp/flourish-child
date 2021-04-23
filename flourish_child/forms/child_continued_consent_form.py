from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
# from flourish_child_validations.form_validators import ChildAssentFormValidator

from ..models import ChildContinuedConsent


class ChildContinuedConsentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

#     form_validator_cls = ChildAssentFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ChildContinuedConsent
        fields = '__all__'
