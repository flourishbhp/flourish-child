from django import forms
from edc_appointment.form_validators import AppointmentFormValidator
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import Appointment


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    """Note, the appointment is only changed, never added,
    through this form.
    """

    appointment_model = 'flourish_child.appointment'

    form_validator_cls = AppointmentFormValidator

    class Meta:
        model = Appointment
        fields = '__all__'
