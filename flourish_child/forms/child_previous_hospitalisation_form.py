from django import forms
from django.core.exceptions import ValidationError
from edc_constants.constants import NO
from flourish_child_validations.form_validators import (
    ChildPreviousHospitalisationFormValidator,
    ChildPreHospitalisationInlineFormValidator)

from ..models import (ChildPreviousHospitalization,
                      ChildPreHospitalizationInline)
from .child_form_mixin import ChildModelFormMixin


class ChildPreviousHospitalizationForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildPreviousHospitalisationFormValidator

    def clean(self):
        super().clean()

        total_inlines = self.data.get(
            'childprehospitalizationinline_set-TOTAL_FORMS')
        hospitalized_count = self.cleaned_data.get('hospitalized_count')
        hos_last_visit = self.cleaned_data.get('hos_last_visit')
        child_hospitalized = self.cleaned_data.get('child_hospitalized')

        if (hos_last_visit == NO or child_hospitalized == NO) and int(total_inlines) > 0:
            msg = 'Please remove inline, The child was never hospitalised'
            raise ValidationError(msg)

        if hospitalized_count != int(total_inlines) and hospitalized_count:
            msg = {
                'hospitalized_count':
                    'Times child hospitalized should match number of inlines'
                }
            raise ValidationError(msg)
        for i in range(int(total_inlines)):
            name_hospital = self.data.get(
                'childprehospitalizationinline_set-' + str(i) + '-name_hospital')
            if not name_hospital:
                raise forms.ValidationError('Please complete the Children/'
                                            'Adolescents Previous Hospital '
                                            'inline form')

    class Meta:
        model = ChildPreviousHospitalization
        fields = '__all__'


class ChildPreHospitalizationInlineForm(ChildModelFormMixin):
    form_validator_cls = ChildPreHospitalisationInlineFormValidator

    class Meta:
        model = ChildPreHospitalizationInline
        fields = '__all__'
