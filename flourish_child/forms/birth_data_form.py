from django.apps import apps as django_apps
from django import forms

from flourish_child_validations.form_validators import BirthDataFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import BirthData


class BirthDataForm(ChildModelFormMixin):
    form_validator_cls = BirthDataFormValidator

    gestational_age = forms.IntegerField(
        label="What is the infant's determined gestational age: ",
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(BirthDataForm, self).__init__(*args, **kwargs)
        self.initial['gestational_age'] = self.get_ga_confirmed

    @property
    def get_ga_confirmed(self):
        if self.get_latest_ultrasound:
            return self.get_latest_ultrasound.ga_confirmed

    @property
    def ultrasound_model_cls(self):
        return django_apps.get_model('flourish_caregiver.ultrasound')

    @property
    def get_latest_ultrasound(self):
        try:
            return self.ultrasound_model_cls.objects.filter(
                maternal_visit__appointment__subject_identifier=
                self.caregiver_subject_identifier).order_by(
                '-report_datetime').first()
        except self.ultrasound_model_cls.DoesNotExist:
            return None

    class Meta:
        model = BirthData
        fields = '__all__'
