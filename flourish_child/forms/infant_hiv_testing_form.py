from django import forms
# from flourish_form_validations.form_validators import HIVInfantTestingFormValidator

from ..models import InfantHIVTesting
from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin


class InfantHIVTestingForm(SubjectModelFormMixin, forms.ModelForm):
    # form_validator_cls = HIVInfantTestingFormValidator

    class Meta:
        model = InfantHIVTesting
        fields = '__all__'
