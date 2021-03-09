from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ChildDummySubjectConsent


class ChildDummySubjectConsentForm(SiteModelFormMixin, FormValidatorMixin,
                                   forms.ModelForm):

    class Meta:
        model = ChildDummySubjectConsent
        fields = '__all__'
