from flourish_child_validations.form_validators import TbPresenceHouseholdMembersAdolFormValidator
from ..models import TbPresenceHouseholdMembersAdol
from .child_form_mixin import ChildModelFormMixin


class TbPresenceHouseholdMembersAdolForm(ChildModelFormMixin):
    form_validator_cls = TbPresenceHouseholdMembersAdolFormValidator

    class Meta:
        model = TbPresenceHouseholdMembersAdol
        fields = '__all__'
