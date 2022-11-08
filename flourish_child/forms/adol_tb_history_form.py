from django import forms
# from flourish_form_validation.form_validators import TbHistoryAdolFormValidator
from ..models import TbHistoryAdol
from .child_form_mixin import ChildModelFormMixin


class TbHistoryAdolForm(ChildModelFormMixin):
    # form_validator_cls = TbHistoryAdolFormValidator

    class Meta:
        model = TbHistoryAdol
        fields = '__all__'
