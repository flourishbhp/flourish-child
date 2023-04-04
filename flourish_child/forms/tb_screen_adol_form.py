from django import forms
from ..models import TbVisitScreeningAdolescent
from .child_form_mixin import ChildModelFormMixin
from flourish_child_validations.form_validators import TbVisitScreeningFormValidator


class TbVisitScreeningAdolescentForm(ChildModelFormMixin):
    form_validator_cls = TbVisitScreeningFormValidator

    class Meta:
        model = TbVisitScreeningAdolescent
        fields = '__all__'
