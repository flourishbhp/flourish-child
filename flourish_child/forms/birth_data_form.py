from django.apps import apps as django_apps
from django import forms

from flourish_child_validations.form_validators import BirthDataFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import BirthData


class BirthDataForm(ChildModelFormMixin):
    form_validator_cls = BirthDataFormValidator

    gestational_age = forms.DecimalField(
        label="What is the infant's determined gestational age: ",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(BirthDataForm, self).__init__(*args, **kwargs)
        self.subject_identifier = self.initial.get('subject_identifier')
        if self.antenatal_enrolment_obj:
            self.initial['gestational_age'] = self.antenatal_enrolment_obj.real_time_ga
        elif self.get_ga_confirmed:
            self.initial['gestational_age'] = self.get_ga_confirmed

    antenatal_enrolment_model = 'flourish_caregiver.antenatalenrollment'

    @property
    def get_ga_confirmed(self):
        if self.get_latest_ultrasound:
            return self.get_latest_ultrasound.ga_confirmed

    @property
    def ultrasound_model_cls(self):
        return django_apps.get_model('flourish_caregiver.ultrasound')

    @property
    def antenatal_enrolment_cls(self):
        return django_apps.get_model(self.antenatal_enrolment_model)

    @property
    def get_latest_ultrasound(self):
        try:
            return self.ultrasound_model_cls.objects.filter(
                child_subject_identifier=self.subject_identifier,
                maternal_visit__appointment__subject_identifier=(
                    self.caregiver_subject_identifier)).order_by(
                '-report_datetime').first()
        except self.ultrasound_model_cls.DoesNotExist:
            return None

    @property
    def antenatal_enrolment_obj(self):
        try:
            antenatal_enrolment_obj = self.antenatal_enrolment_cls.objects.get(
                child_subject_identifier=self.subject_identifier,
                subject_identifier=self.caregiver_subject_identifier)
        except self.antenatal_enrolment_cls.DoesNotExist:
            return None
        else:
            return antenatal_enrolment_obj

    class Meta:
        model = BirthData
        fields = '__all__'
