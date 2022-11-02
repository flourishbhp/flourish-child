from django import forms
# from flourish_form_validation.form_validators import TbVisitScreeningAdolescentFormValidator
from ..models import TbVisitScreeningAdolescent
from .child_form_mixin import ChildModelFormMixin


class TbVisitScreeningAdolescentForm(ChildModelFormMixin):
    # form_validator_cls = TbVisitScreeningAdolescentFormValidator

    class Meta:
        model = TbVisitScreeningAdolescent
        fields = '__all__'
