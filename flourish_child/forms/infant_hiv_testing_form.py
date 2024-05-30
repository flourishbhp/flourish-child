from django import forms

from flourish_child_validations.form_validators import \
    InfantHIVTestingAdminFormValidatorRepeat, InfantHIVTestingFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import (InfantHIVTesting, InfantHIVTesting18Months,
                      InfantHIVTesting9Months,
                      InfantHIVTestingAfterBreastfeeding, InfantHIVTestingAge6To8Weeks,
                      InfantHIVTestingBirth,
                      InfantHIVTestingOther)


class InfantHIVTestingForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingFormValidator

    class Meta:
        model = InfantHIVTesting
        fields = '__all__'


class InfantHIVTestingAfterBreastfeedingForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTestingAfterBreastfeeding
        fields = '__all__'


class InfantHIVTestingAge6To8WeeksForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTestingAge6To8Weeks
        fields = '__all__'


class InfantHIVTesting9MonthsForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTesting9Months
        fields = '__all__'


class InfantHIVTesting18MonthsForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTesting18Months
        fields = '__all__'


class InfantHIVTestingBirthForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTestingBirth
        fields = '__all__'


class InfantHIVTestingOtherForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    child_age = forms.DecimalField(
        label='Child age',
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={'readonly': True}),
        decimal_places=1, )

    class Meta:
        model = InfantHIVTestingOther
        fields = '__all__'
