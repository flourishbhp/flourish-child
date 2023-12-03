from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models import ChildTBReferralOutcome
from flourish_form_validations.form_validators.caregiver_tb_screening_form_validator \
    import CaregiverTBScreeningFormValidator


class ChildTBReferralOutcomeForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = CaregiverTBScreeningFormValidator

    class Meta:
        model = ChildTBReferralOutcome
        fields = '__all__'
