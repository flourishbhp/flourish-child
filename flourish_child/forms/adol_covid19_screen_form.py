from django import forms
# from flourish_form_validation.form_validators import Covid19FormValidator
from ..models import Covid19
from .child_form_mixin import ChildModelFormMixin


class Covid19Form(ChildModelFormMixin):
    # form_validator_cls = Covid19FormValidator

    class Meta:
        model = Covid19
        fields = '__all__'
