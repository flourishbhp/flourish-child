from django import forms

from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_child_validations.form_validators import \
    InfantHIVTestingAdminFormValidatorRepeat, InfantHIVTestingFormValidator
from ..models import (InfantHIVTesting, InfantHIVTesting18Months,
                      InfantHIVTesting9Months,
                      InfantHIVTestingAfterBreastfeeding, InfantHIVTestingAge6To8Weeks,
                      InfantHIVTestingBirth,
                      InfantHIVTestingOther)


class InfantHIVTestingForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingFormValidator

    class Meta:
        model = InfantHIVTesting
        fields = '__all__'


class InfantHIVTestingAfterBreastfeedingForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTestingAfterBreastfeeding
        fields = '__all__'


class InfantHIVTestingAge6To8WeeksForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTestingAge6To8Weeks
        fields = '__all__'


class InfantHIVTesting9MonthsForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTesting9Months
        fields = '__all__'


class InfantHIVTesting18MonthsForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTesting18Months
        fields = '__all__'


class InfantHIVTestingBirthForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTestingBirth
        fields = '__all__'


class InfantHIVTestingOtherForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    class Meta:
        model = InfantHIVTestingOther
        fields = '__all__'
