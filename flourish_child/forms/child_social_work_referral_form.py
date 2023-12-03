from django import forms
from flourish_child_validations.form_validators.child_social_work_referral_form_validator import ChildSocialWorkReferralValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildSocialWorkReferral
from django.apps import apps as django_apps


class ChildSocialWorkReferralForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildSocialWorkReferralValidator

    caregiver_child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    antenatal_model = 'flourish_caregiver.antenatalenrollment'

    @property
    def caregiver_child_consent_model_cls(self):
        return django_apps.get_model(self.caregiver_child_consent_model)

    @property
    def antenatal_model_cls(self):
        return django_apps.get_model(self.antenatal_model)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        child_subject_identifier = self.initial.get('subject_identifier', None)

        if child_subject_identifier:
            caregiver_child_consent_obj = self.caregiver_child_consent_model_cls.objects.filter(
                subject_identifier=child_subject_identifier).latest('consent_datetime')
            antenatal_enrol_obj = self.antenatal_model_cls.objects.filter(
                child_subject_identifier=child_subject_identifier).first()

            if antenatal_enrol_obj:
                if antenatal_enrol_obj.current_hiv_status == 'POS':
                    self.initial['child_exposure_status'] = 'heu'
            elif caregiver_child_consent_obj.child_dataset:
                if caregiver_child_consent_obj.child_dataset.infant_hiv_exposed == 'Exposed' or caregiver_child_consent_obj.child_dataset.infant_hiv_exposed == 'exposed':
                    self.initial['child_exposure_status'] = 'heu'
            else:
                self.initial['child_exposure_status'] = 'huu'

    class Meta:
        model = ChildSocialWorkReferral
        fields = '__all__'
