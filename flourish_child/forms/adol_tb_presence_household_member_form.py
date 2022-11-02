from django import forms
# from flourish_form_validation.form_validators import TbPresenceHouseholdMembersFormValidator
from ..models import TbPresenceHouseholdMembers
from .child_form_mixin import ChildModelFormMixin


class TbPresenceHouseholdMembersForm(ChildModelFormMixin):
    # form_validator_cls = TbPresenceHouseholdMembersFormValidator

    class Meta:
        model = TbPresenceHouseholdMembers
        fields = '__all__'
