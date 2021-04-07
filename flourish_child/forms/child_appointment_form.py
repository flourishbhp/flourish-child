from django import forms
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import Appointment


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    """Note, the appointment is only changed, never added,
    through this form.
    """

    appointment_model = 'flourish_child.appointment'

    class Meta:
        model = Appointment
        fields = '__all__'
