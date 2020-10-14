from django import forms

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildImmunizationHistory, VaccinesMissed, VaccinesReceived


class ChildImmunizationHistoryForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildImmunizationHistory
        fields = '__all__'


class VaccinesReceivedForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = VaccinesReceived
        fields = '__all__'


class VaccinesMissedForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = VaccinesMissed
        fields = '__all__'
