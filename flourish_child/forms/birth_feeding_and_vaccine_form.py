import datetime
from django import forms
from django.core.exceptions import ValidationError

from flourish_child_validations.form_validators import BirthFeedingAndVaccineFormValidator


from ..models import BirthFeedingVaccine, BirthVaccines, ChildBirth
from .child_form_mixin import ChildModelFormMixin


class BirthFeedingVaccineForm(ChildModelFormMixin):

    form_validator_cls = BirthFeedingAndVaccineFormValidator

    def validate_against_birth_date(self, subject_identifier=None,
                                    vaccine_date=None, vaccine_name=None):

        try:
            infant_birth = ChildBirth.objects.get(
                subject_identifier=subject_identifier)
        except self.ChildBirth.DoesNotExist:
            raise ValidationError('Please complete Child Birth form '
                                  'before proceeding.')
        else:
            infant_dob = infant_birth.dob
            if vaccine_date and infant_dob:
                if vaccine_date < infant_dob:
                    raise forms.ValidationError(
                        'The date vaccine was given should not be before the '
                        f'delivery date. Got vaccine {vaccine_name} and date {vaccine_date}'
                        f' but delivery date is {infant_dob}'
                    )

    def clean(self):
        super().clean()
        self.subject_identifier = self.cleaned_data.get(
            'child_visit').appointment.subject_identifier

        self.validate_vaccine_date_against_birth_date()

    def validate_vaccine_date_against_birth_date(self):
        subject_identifier = self.cleaned_data.get(
            'child_visit').subject_identifier
        total = self.data.get('infantvaccines_set-TOTAL_FORMS')
        if total is not None:
            for i in range(int(total)):
                vaccine_date = self.data.get(
                    'infantvaccines_set-' + str(i) + '-vaccine_date')
                vaccine_name = self.data.get(
                    'infantvaccines_set-' + str(i) + '-vaccination')
                if vaccine_name and vaccine_date:
                    vaccine_date = datetime.datetime.strptime(
                        vaccine_date, '%Y-%m-%d')
                    self.validate_against_birth_date(
                        subject_identifier, vaccine_date.date(), vaccine_name)

    class Meta:
        model = BirthFeedingVaccine
        fields = '__all__'


class BirthVaccinesForm(forms.ModelForm):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'birth_feed_vaccine').child_visit.appointment.subject_identifier
        super().clean()

    class Meta:
        model = BirthVaccines
        fields = '__all__'
