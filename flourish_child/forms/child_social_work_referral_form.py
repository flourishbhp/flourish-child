from django import forms
from flourish_child_validations.form_validators.child_social_work_referral_form_validator import ChildSocialWorkReferralValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildSocialWorkReferral


class ChildSocialWorkReferralForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildSocialWorkReferralValidator

    class Meta:
        model = ChildSocialWorkReferral
        fields = '__all__'
