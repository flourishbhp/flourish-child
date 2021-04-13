from django import forms

from edc_constants.constants import OTHER, YES
from flourish_child_validations.form_validators import VaccinesReceivedFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildImmunizationHistory, VaccinesMissed, VaccinesReceived


class ChildImmunizationHistoryForm(ChildModelFormMixin, forms.ModelForm):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'child_visit').appointment.subject_identifier

        super().clean()

        received_vaccine_name = self.data.get(
            'vaccinesreceived_set-0-received_vaccine_name')

        if not received_vaccine_name:
            msg = 'Please complete the table for vaccines received.'
            raise forms.ValidationError(msg)

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
