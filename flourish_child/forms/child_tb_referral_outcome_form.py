from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models import ChildTBReferralOutcome
from flourish_child_validations.form_validators import ChildTBReferralOutcomeFormValidator


class ChildTBReferralOutcomeForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildTBReferralOutcomeFormValidator

    class Meta:
        model = ChildTBReferralOutcome
        fields = '__all__'
