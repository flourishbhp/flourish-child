from django import forms
from edc_constants.constants import NO, YES

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child_validations.form_validators import \
    ChildHospitalizationFormValidations, AdmissionsReasonFormValidations
from ..models.child_hospitalization import ChildHospitalization, \
    AdmissionsReasons


class ChildHospitalizationForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildHospitalizationFormValidations

    def clean(self):
        cleaned_data = super().clean()

        total_num_hosp = int(
            self.data.get('admissionsreasons_set-TOTAL_FORMS'))

        if cleaned_data.get('number_hospitalised') != total_num_hosp:
            raise forms.ValidationError(
                {'number_hospitalised': 'Must be equal to the number of inlines'})

        if cleaned_data.get('hospitalized') == NO and total_num_hosp:
            raise forms.ValidationError('Admissions information is not required if'
                                        ' child was not hospitalized since last FLOURISH'
                                        ' visit.')
        elif cleaned_data.get('hospitalized') == YES and not total_num_hosp:
            raise forms.ValidationError('Admissions information is required if'
                                        ' child was hospitalized since last FLOURISH'
                                        ' visit.')

    class Meta:
        model = ChildHospitalization
        fields = '__all__'


class AdmissionsReasonsForms(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = AdmissionsReasonFormValidations

    class Meta:
        model = AdmissionsReasons
        fields = '__all__'
