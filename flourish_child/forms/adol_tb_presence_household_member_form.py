from django import forms
# from flourish_form_validation.form_validators import TbPresenceHouseholdMembersAdolFormValidator
from ..models import TbPresenceHouseholdMembersAdol
from .child_form_mixin import ChildModelFormMixin


class TbPresenceHouseholdMembersAdolForm(ChildModelFormMixin):
    # form_validator_cls = TbPresenceHouseholdMembersAdolFormValidator

    class Meta:
        model = TbPresenceHouseholdMembersAdol
        fields = '__all__'
