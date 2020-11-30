from ..models import InfantArvExposure
from .child_form_mixin import ChildModelFormMixin


class InfantArvExposureForm(ChildModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = InfantArvExposure
        fields = '__all__'
