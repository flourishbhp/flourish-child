from django import forms
# from flourish_form_validation.form_validators import TbRoutineScreenAdolescentFormValidator
from ..models import TbRoutineScreenAdol
from .child_form_mixin import ChildModelFormMixin
from flourish_child_validations.form_validators import TbScreeningDuringEncountersFormValidator

class TbRoutineScreenAdolForm(ChildModelFormMixin):
    form_validator_cls = TbScreeningDuringEncountersFormValidator

    class Meta:
        model = TbRoutineScreenAdol
        fields = '__all__'
