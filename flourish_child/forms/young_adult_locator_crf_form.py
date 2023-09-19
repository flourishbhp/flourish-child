
from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from .child_form_mixin import ChildModelFormMixin

from ..models import YoungAdultLocatorCrf


class YoungAdultLocatorCrfForm(ChildModelFormMixin,
                               forms.ModelForm):
    class Meta:
        model = YoungAdultLocatorCrf
        fields = '__all__'
