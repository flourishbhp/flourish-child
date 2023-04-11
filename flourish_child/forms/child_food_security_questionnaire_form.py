from django import forms

from flourish_child_validations.form_validators import \
    ChildFoodSecurityQuestionnaireFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildFoodSecurityQuestionnaire


class ChildFoodSecurityQuestionnaireForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildFoodSecurityQuestionnaireFormValidator

    class Meta:
        model = ChildFoodSecurityQuestionnaire
        fields = '__all__'
