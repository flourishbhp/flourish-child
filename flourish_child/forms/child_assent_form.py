from django import forms
from django.apps import apps as django_apps
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_child_validations.form_validators import ChildAssentFormValidator

from ..models import ChildAssent


class ChildAssentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ChildAssentFormValidator

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        subject_identifier = self.initial.get('subject_identifier', None) \
            or instance.subject_identifier \
            or args[0].get('subject_identifier', None) \
            or self.cleaned_data.get('subject_identifier', None)

        child_consent = self.get_caregiver_child_consent(
            subject_identifier=subject_identifier)

        if instance and instance.id:
            for key in self.fields.keys():
                self.fields[key].disabled = True
        elif not instance.id and child_consent:
            self.initial.update(
                self.assent_initial_values(child_consent=child_consent))

    def get_caregiver_child_consent(self, subject_identifier=None):
        child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        consents = child_consent_cls.objects.filter(
            subject_identifier=subject_identifier)

        return consents.latest('consent_datetime')

    def get_latest_consent_version(self, screening_identifier=None):
        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

        try:
            consent_version_cls.objects.get(
                screening_identifier=screening_identifier)
        except consent_version_cls.DoesNotExist:
            raise forms.ValidationError(
                'Please complete the consent version form before proceeding.')

    def assent_initial_values(self, child_consent=None):
        initials = {}
        fields = ['screening_identifier', 'first_name', 'last_name', 'gender',
                  'identity', 'identity_type', 'confirm_identity', 'dob']
        if child_consent:
            for field in fields:
                if field == 'screening_identifier':
                    initials.update({field: getattr(
                        child_consent.subject_consent, field)})
                    continue
                elif field == 'dob':
                    initials.update({field: getattr(child_consent, 'child_dob')})
                    continue
                initials.update({field: getattr(child_consent, field)})
            first_name = getattr(child_consent, 'first_name')
            last_name = getattr(child_consent, 'last_name')
            initials.update(
                {'initials': self.set_initials(first_name=first_name, last_name=last_name)})
        return initials

    def set_initials(self, first_name=None, last_name=None):
        initials = ''
        if first_name and last_name:
            if (len(first_name.split(' ')) > 1):
                first = first_name.split(' ')[0]
                middle = first_name.split(' ')[1]
                initials = f'{first[:1]}{middle[:1]}{last_name[:1]}'
            else:
                initials = f'{first_name[:1]}{last_name[:1]}'
        return initials

    class Meta:
        model = ChildAssent
        fields = '__all__'
