from flourish_child_validations.form_validators import AnthropometricFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import AdolescentClinicalMeasurements


class AdolClinicalMeasurementsForm(ChildModelFormMixin):
    form_validator_cls = AnthropometricFormValidator

    class Meta:
        model = AdolescentClinicalMeasurements
        fields = '__all__'
