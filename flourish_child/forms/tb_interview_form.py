from django import forms

from flourish_form_validations.form_validators import TbInterviewFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import TbAdolInterview


class TbInterviewForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = TbInterviewFormValidator

    class Meta:
        model = TbAdolInterview
        fields = '__all__'
