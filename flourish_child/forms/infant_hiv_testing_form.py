from django import forms
from edc_visit_tracking.constants import UNSCHEDULED

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


class InfantHIVTestsFormMixin(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = InfantHIVTestingAdminFormValidatorRepeat

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance')
        previous_instance = getattr(self, 'previous_instance', None)

        child_visit_id = initial.get(
            'child_visit', args[0]['child_visit'] if args else None)

        try:
            child_visit_obj = self.visit_model.objects.get(id=child_visit_id)
        except self.visit_model.DoesNotExist:
            child_visit_obj = None
        else:
            if (not instance and previous_instance and child_visit_obj.reason ==
                    UNSCHEDULED):
                for key in self.base_fields.keys():
                    if key not in ['child_visit', 'report_datetime', 'hiv_test_result']:
                        initial[key] = getattr(previous_instance, key)

        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)


class InfantHIVTestingAfterBreastfeedingForm(InfantHIVTestsFormMixin, forms.ModelForm):
    class Meta:
        model = InfantHIVTestingAfterBreastfeeding
        fields = '__all__'


class InfantHIVTestingAge6To8WeeksForm(InfantHIVTestsFormMixin, forms.ModelForm):
    class Meta:
        model = InfantHIVTestingAge6To8Weeks
        fields = '__all__'


class InfantHIVTesting9MonthsForm(InfantHIVTestsFormMixin, forms.ModelForm):
    class Meta:
        model = InfantHIVTesting9Months
        fields = '__all__'


class InfantHIVTesting18MonthsForm(InfantHIVTestsFormMixin, forms.ModelForm):
    class Meta:
        model = InfantHIVTesting18Months
        fields = '__all__'


class InfantHIVTestingBirthForm(InfantHIVTestsFormMixin, forms.ModelForm):
    class Meta:
        model = InfantHIVTestingBirth
        fields = '__all__'


class InfantHIVTestingOtherForm(InfantHIVTestsFormMixin, forms.ModelForm):
    child_age = forms.DecimalField(
        label='Child age',
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={'readonly': True}),
        decimal_places=1, )

    class Meta:
        model = InfantHIVTestingOther
        fields = '__all__'
