from django import forms
from django.forms import BaseInlineFormSet

from edc_constants.constants import OTHER, YES
from flourish_child_validations.form_validators import VaccinesReceivedFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildImmunizationHistory, VaccinesMissed, VaccinesReceived


class ChildImmunizationHistoryForm(ChildModelFormMixin, forms.ModelForm):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'child_visit').appointment.subject_identifier

        super().clean()

        rec_add_immunization = self.cleaned_data.get('rec_add_immunization')
        received_vaccine_name = self.data.get(
            'vaccinesreceived_set-0-received_vaccine_name')
        if rec_add_immunization:
            self.validate_add_immunization(rec_add_immunization, received_vaccine_name)
        else:
            vaccines_received = self.data.get(
                'vaccinesreceived_set-0-received_vaccine_name')
            if self.data.get('vaccines_received') == YES:
                if not vaccines_received:
                    msg = {'vaccines_received':
                               'You mentioned that vaccines were received. Please '
                               'indicate which ones on the Received Vaccines table.'}
                    raise forms.ValidationError(msg)
            else:
                if vaccines_received:
                    raise forms.ValidationError(
                        'No vaccines received. Do not fill Received Vaccines '
                        'table')
    
        missed_vaccine_name = self.data.get(
            'vaccinesmissed_set-0-missed_vaccine_name')
        if self.data.get('vaccines_missed') == YES:
            if not missed_vaccine_name:
                msg = {'vaccines_missed':
                           'You mentioned that the child missed some '
                           'vaccines. Please indicate which ones in '
                           'the Missed Vaccines table.'}
                raise forms.ValidationError(msg)
        else:
            if missed_vaccine_name:
                raise forms.ValidationError(
                    'No vaccines missed. Do not fill Missed Vaccines table')
    
        missed_vaccines = self.data.get('vaccinesmissed_set-TOTAL_FORMS')
        for i in range(int(missed_vaccines)):
            reason_missed = self.data.get(
                'vaccinesmissed_set-' + str(i) + '-reason_missed')
            other_reason = self.data.get(
                'vaccinesmissed_set-' + str(i) + '-reason_missed_other')
    
            if reason_missed == OTHER and not other_reason:
                message = {
                    'vaccines_missed': 'Please specify other reasons missed'
                                       ' in the table below'
                }
                raise forms.ValidationError(message)
    
    def validate_add_immunization(self, add_immunization, vaccine_name):
        if add_immunization == YES:
            if not vaccine_name:
                msg = {'rec_add_immunization':
                           'You stated that the child has additional immunizations '
                           'received. Please complete the table for vaccines received.'}
                raise forms.ValidationError(msg)
        else:
            if vaccine_name:
                msg = {'rec_add_immunization':
                           'No additional immunizations received. Do not fill table '
                           'for vaccines received'}
                raise forms.ValidationError(msg)

    class Meta:
        model = ChildImmunizationHistory
        fields = '__all__'


class VaccinesReceivedForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = VaccinesReceivedFormValidator

    class Meta:
        model = VaccinesReceived
        fields = '__all__'


class VaccinesMissedForm(ChildModelFormMixin, forms.ModelForm):
    class Meta:
        model = VaccinesMissed
        fields = '__all__'


class VaccinesReceivedInlineFormSet(BaseInlineFormSet):
    model = VaccinesReceived

    def __init__(self, *args, **kwargs):
        super(VaccinesReceivedInlineFormSet, self).__init__(*args, **kwargs)
        subject_identifier = self.request.GET.get('subject_identifier', None)
        self.initial = []
        if subject_identifier:
            immunization_obj = ChildImmunizationHistory.objects.filter(
                child_visit__subject_identifier=subject_identifier).earliest('report_datetime')

            vaccines_received = immunization_obj.vaccinesreceived_set.all()

            if vaccines_received:
                for vaccine_received in vaccines_received:
                    self.initial.append({
                        'received_vaccine_name': vaccine_received.received_vaccine_name,
                        'first_dose_dt': vaccine_received.first_dose_dt,
                        'second_dose_dt': vaccine_received.second_dose_dt,
                        'third_dose_dt': vaccine_received.third_dose_dt,
                        'booster_dose_dt': vaccine_received.booster_dose_dt,

                    })

        self.extra = len(self.initial) or 3


class VaccinesMissedInlineFormSet(BaseInlineFormSet):
    model = VaccinesMissed

    def __init__(self, *args, **kwargs):
        super(VaccinesMissedInlineFormSet, self).__init__(*args, **kwargs)
        subject_identifier = self.request.GET.get('subject_identifier', None)
        self.initial = []
        if subject_identifier:
            immunization_obj = ChildImmunizationHistory.objects.filter(
                child_visit__subject_identifier=subject_identifier).earliest('report_datetime')

            vaccines_missed = immunization_obj.vaccinesmissed_set.all()

            for vaccine_missed in vaccines_missed:
                self.initial.append({
                    'missed_vaccine_name': vaccine_missed.missed_vaccine_name,
                    'reason_missed': vaccine_missed.reason_missed,
                    'reason_missed_other': vaccine_missed.reason_missed_other
                })

        self.extra = len(self.initial)
