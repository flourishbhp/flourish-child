from django import forms
from django.apps import apps as django_apps
from edc_form_validators import FormValidatorMixin

from flourish_child.models.pre_flourish_birth_data import PreFlourishBirthData
from flourish_child_validations.form_validators import \
    PreFlourishBirthDataFormValidator


class PreFlourishBirthDataForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PreFlourishBirthDataFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subject_identifier = None

        if self.initial:
            subject_identifier = self.initial.get('subject_identifier', None)

        if subject_identifier:
            child_consent = self.get_caregiver_child_consent(
                subject_identifier=subject_identifier)
            if child_consent:
                self.initial.update({
                    'dob': child_consent.child_dob,
                })

    def get_caregiver_child_consent(self, subject_identifier=None):
        child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')
        if subject_identifier:
            try:
                consents = child_consent_cls.objects.filter(
                    subject_identifier=subject_identifier).latest('consent_datetime')
            except child_consent_cls.DoesNotExist:
                pass
            else:
                return consents

    class Meta:
        model = PreFlourishBirthData
        fields = '__all__'
