from django import forms

# from flourish_form_validations.form_validators import AdolescentClinicalMeasurementsFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import AdolescentClinicalMeasurements


class AdolClinicalMeasurementsForm(ChildModelFormMixin):
    # form_validator_cls = AdolescentClinicalMeasurementsFormValidator

    class Meta:
        model = AdolescentClinicalMeasurements
        fields = '__all__'
