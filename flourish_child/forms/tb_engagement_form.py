from django import forms

from flourish_form_validations.form_validators import TbEngagementFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import TbAdolEngagement


class TbEngagementForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = TbEngagementFormValidator

    class Meta:
        model = TbAdolEngagement
        fields = '__all__'
