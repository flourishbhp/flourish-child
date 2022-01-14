from django import forms

from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_form_validations.form_validators import \
    ChildHospitalizationFormValidations, AdmissionsReasonFormValidations
from ..models.child_hospitalization import ChildHospitalization, \
    AdmissionsReasons


class ChildHospitalisationForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildHospitalizationFormValidations

    def clean(self):
        cleaned_data = super().clean()

        total_num_hosp = int(
            self.data.get('admissionsreasons_set-TOTAL_FORMS'))

        if total_num_hosp != cleaned_data.get(self.data.get(
                'number_hospitalised')):
            raise forms.ValidationError(
                {'number_hospitalised':
                     'Must be equal to the number of inlines'})

    class Meta:
        model = ChildHospitalization
        fields = '__all__'


class AdmissionsReasonsForms(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = AdmissionsReasonFormValidations

    class Meta:
        model = AdmissionsReasons
        fields = '__all__'
