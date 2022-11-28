from django import forms
from flourish_child_validations.form_validators import TbPresenceHouseholdMembersAdolFormValidator
from ..models import HivTestingAdol
from .child_form_mixin import ChildModelFormMixin


class HIVTestingAdolForm(ChildModelFormMixin):
    # form_validator_cls = TbPresenceHouseholdMembersAdolFormValidator

    class Meta:
        model = HivTestingAdol
        fields = '__all__'
