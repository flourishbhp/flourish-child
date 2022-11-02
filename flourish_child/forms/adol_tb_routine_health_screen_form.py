from django import forms
# from flourish_form_validation.form_validators import TbRoutineScreenAdolescentFormValidator
from ..models import TbRoutineScreenAdol
from .child_form_mixin import ChildModelFormMixin


class TbRoutineScreenAdolForm(ChildModelFormMixin):
    # form_validator_cls = TbRoutineScreenAdolescentFormValidator

    class Meta:
        model = TbRoutineScreenAdol
        fields = '__all__'
