from django import forms
from flourish_child_validations.form_validators import TbHistoryFormValidator
from ..models import TbHistoryAdol
from .child_form_mixin import ChildModelFormMixin


class TbHistoryAdolForm(ChildModelFormMixin):
    form_validator_cls = TbHistoryFormValidator

    class Meta:
        model = TbHistoryAdol
        fields = '__all__'
