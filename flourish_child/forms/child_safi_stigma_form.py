from django import forms
from flourish_child_validations.form_validators.child_social_work_referral_form_validator import ChildSocialWorkReferralValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildSafiStigma


class ChildSafiStigmaForm(ChildModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildSafiStigma
        fields = '__all__'
