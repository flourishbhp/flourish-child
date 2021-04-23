from flourish_child_validations.form_validators import BirthDataFormValidator

from ..models import BirthData
from .child_form_mixin import ChildModelFormMixin


class BirthDataForm(ChildModelFormMixin):

    form_validator_cls = BirthDataFormValidator

    class Meta:
        model = BirthData
        fields = '__all__'
