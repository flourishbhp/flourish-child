from django import forms
from django.apps import apps as django_apps
from edc_form_validators import FormValidatorMixin

from flourish_child.models.pre_flourish_birth_data import PreFlourishBirthData
from flourish_child_validations.form_validators import \
    PreFlourishBirthDataFormValidator


class PreFlourishBirthDataForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PreFlourishBirthDataFormValidator
    pre_flourish_child_consent_model = 'pre_flourish.preflourishcaregiverchildconsent'
    child_dataset_cls = django_apps.get_model('flourish_child.childdataset')
    huu_pre_enrollment_cls = django_apps.get_model('pre_flourish.HuuPreEnrollment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject_identifier = None

        if self.initial:
            self.subject_identifier = self.initial.get('subject_identifier', None)

        if self.subject_identifier:
            child_consent = self.get_caregiver_child_consent(
                subject_identifier=self.subject_identifier)
            if child_consent:
                huu_pre_enrollment_obj = self.huu_pre_enrollment_obj(child_consent)
                gestational_age_weeks = getattr(huu_pre_enrollment_obj,
                                                'gestational_age_weeks', None)
                gestational_age_months = getattr(huu_pre_enrollment_obj,
                                                 'gestational_age_months', None)
                self.initial.update({
                    'dob': child_consent.child_dob,
                    'gestational_age_weeks': gestational_age_weeks,
                    'gestational_age_months': gestational_age_months,
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

    def huu_pre_enrollment_obj(self, child_consent):
        if hasattr(child_consent, 'study_child_identifier'):
            try:
                return self.huu_pre_enrollment_cls.objects.get(
                    pre_flourish_visit__subject_identifier=child_consent
                    .study_child_identifier)
            except self.huu_pre_enrollment_cls.DoesNotExist:
                return None

    class Meta:
        model = PreFlourishBirthData
        fields = '__all__'
