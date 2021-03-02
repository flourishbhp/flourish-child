from flourish_child_validations.form_validators import InfantArvExposureFormValidator

from ..models import InfantArvExposure
from .child_form_mixin import ChildModelFormMixin


class InfantArvExposureForm(ChildModelFormMixin):

    form_validator_cls = InfantArvExposureFormValidator

    class Meta:
        model = InfantArvExposure
        fields = '__all__'
