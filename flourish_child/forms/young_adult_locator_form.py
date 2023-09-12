from itertools import chain

from django import forms
from django.db.models import ManyToManyField
from django.apps import apps as django_apps
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import YES
from edc_form_validators import FormValidatorMixin

from ..models import YoungAdultLocator
from flourish_child_validations.form_validators import YoungAdultLocatorFormValidator
from edc_locator.forms import SubjectLocatorForm, SubjectLocatorFormValidator


class YoungAdultLocatorForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    caregiver_child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    form_validator_cls = YoungAdultLocatorFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            subject_consented = self.caregiver_child_consent_cls.objects.filter(
                subject_identifier=self.initial.get('subject_identifier', None)).latest(
                'consent_datetime')
        except self.caregiver_child_consent_cls.DoesNotExist:
            pass
        else:
            self.fields['first_name'].widget = forms.TextInput(
                attrs={'readonly': 'readonly'})
            self.fields['last_name'].widget = forms.TextInput(
                attrs={'readonly': 'readonly'})
            self.initial['first_name'] = subject_consented.first_name
            self.initial['last_name'] = subject_consented.last_name

    @property
    def caregiver_child_consent_cls(self):
        return django_apps.get_model(self.caregiver_child_consent_model)

    class Meta:
        model = YoungAdultLocator
        fields = '__all__'
