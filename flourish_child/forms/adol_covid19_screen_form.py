from django import forms
# from flourish_form_validation.form_validators import Covid19AdolFormValidator
from ..models import Covid19Adol
from .child_form_mixin import ChildModelFormMixin


class Covid19AdolForm(ChildModelFormMixin):
    # form_validator_cls = Covid19AdolFormValidator

    class Meta:
        model = Covid19Adol
        fields = '__all__'
