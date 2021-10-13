from ..models import InfantFeeding
from .child_form_mixin import ChildModelFormMixin

from flourish_child_validations.form_validators import InfantFeedingFormValidator


class InfantFeedingForm(ChildModelFormMixin):

    form_validator_cls = InfantFeedingFormValidator

    class Meta:
        model = InfantFeeding
        fields = '__all__'
