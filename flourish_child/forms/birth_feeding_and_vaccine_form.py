from django import forms

from ..models import BirthFeedingVaccine, BirthVaccines
from .child_form_mixin import ChildModelFormMixin


class BirthFeedingVaccineForm(ChildModelFormMixin):

    form_validator_cls = None

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
