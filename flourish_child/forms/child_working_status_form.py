from django import forms
from flourish_child_validations.form_validators import ChildWorkingStatusFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildWorkingStatus


class ChildWorkingStatusForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildWorkingStatusFormValidator

    class Meta:
        model = ChildWorkingStatus
        fields = '__all__'
