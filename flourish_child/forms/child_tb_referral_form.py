from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models.child_tb_referral import ChildTBReferral
from flourish_child_validations.form_validators.child_tb_referral_form_validator import \
    ChildTBReferralFormValidator


class ChildTBReferralForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildTBReferralFormValidator

    class Meta:
        model = ChildTBReferral
        fields = '__all__'
