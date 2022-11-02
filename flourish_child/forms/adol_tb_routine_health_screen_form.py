from django import forms
# from flourish_form_validation.form_validators import TbRoutineScreenAdolescentFormValidator
from ..models import TbRoutineScreenAdolescent
from .child_form_mixin import ChildModelFormMixin


class TbRoutineScreenAdolescentForm(ChildModelFormMixin):
    # form_validator_cls = TbRoutineScreenAdolescentFormValidator

    class Meta:
        model = TbRoutineScreenAdolescent
        fields = '__all__'
