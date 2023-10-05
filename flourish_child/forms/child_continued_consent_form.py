from django import forms
from django.forms import model_to_dict
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
        subject_identifier = initial.get('subject_identifier', None)

        if subject_identifier:
            try:
                child_assent = ChildAssent.objects.filter(
                    subject_identifier=subject_identifier
                    ).latest('consent_datetime')
            except ChildAssent.DoesNotExist:
                raise forms.ValidationError(
                    'Child assent for this child is missing. Please complete form')
            else:
                # Fields that exist in both forms
                fields = set(self.base_fields.keys()) \
                    & set(model_to_dict(child_assent).keys())

                for key in fields:
                    if key not in ['subject_identifier', 'consent_datetime', ]:
                        initial[key] = getattr(child_assent, key)
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    class Meta:
        model = ChildContinuedConsent
        fields = '__all__'
