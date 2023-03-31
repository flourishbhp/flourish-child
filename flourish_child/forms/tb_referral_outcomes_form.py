from django import forms

from flourish_child_validations.form_validators import TbReferralOutcomesFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import TbAdolReferralOutcomes


class TbReferralOutcomesForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = TbReferralOutcomesFormValidator

    class Meta:
        model = TbAdolReferralOutcomes
        fields = '__all__'
