from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_child_validations.form_validators import ChildContinuedConsentFormValidator

from ..models import ChildContinuedConsent, ChildAssent


class ChildContinuedConsentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ChildContinuedConsentFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        subject_identifier = initial.get('subject_identifier')
        if subject_identifier:
            try:
                child_assent = ChildAssent.objects.get(
                    subject_identifier=subject_identifier)
            except ChildAssent.DoesNotExist:
                raise forms.ValidationError(
                    'Child assent for this child is missing. Please complete form')
            else:
                for key in self.base_fields.keys():
                    if key not in ['subject_identifier', 'consent_datetime']:
                        initial[key] = getattr(child_assent, key)
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    class Meta:
        model = ChildContinuedConsent
        fields = '__all__'
