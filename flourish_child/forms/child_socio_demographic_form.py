from flourish_child_validations.form_validators import ChildSocioDemographicFormValidator

from ..models import ChildSocioDemographic
from .child_form_mixin import ChildModelFormMixin


class ChildSocioDemographicForm(ChildModelFormMixin):

    form_validator_cls = ChildSocioDemographicFormValidator

    class Meta:
        model = ChildSocioDemographic
        fields = '__all__'
