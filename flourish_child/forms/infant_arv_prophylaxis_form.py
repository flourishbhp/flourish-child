from django import forms
from edc_constants.constants import YES, NO
from flourish_child_validations.form_validators import InfantArvProphylaxisFormValidator

from ..models import InfantArvProphylaxis, ChildArvProphDates
from .child_form_mixin import ChildModelFormMixin


class InfantArvProphylaxisForm(ChildModelFormMixin):

    form_validator_cls = InfantArvProphylaxisFormValidator

    def clean(self):
        super().clean()

        took_art_proph = self.cleaned_data.get('took_art_proph', None)

        arvs_took_name = self.data.get(
            'childarvprophdates_set-0-arv_name')

        if took_art_proph == YES and not arvs_took_name:
            message = {'took_art_proph':
                       'The baby took some ARVs please complete table for each'
                       ' ARV, start date and stop date.'}
            raise forms.ValidationError(message)
        elif took_art_proph == NO and arvs_took_name:
            message = {'took_art_proph':
                       'The baby did not take any ARVs do not complete table'
                       ' for ARVs, start date and stop date.'}
            raise forms.ValidationError(message)
            
        

    class Meta:
        model = InfantArvProphylaxis
        fields = '__all__'


class ChildArvProphDatesForm(ChildModelFormMixin):
    class Meta:
        model = ChildArvProphDates
        fields = '__all__'
