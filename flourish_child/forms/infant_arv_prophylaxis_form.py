from django import forms
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

        if took_art_proph and not arvs_took_name:
            message = {'took_art_proph':
                       'The baby took some ARVs please complete dates for each ARV'}
            self._errors.update(message)
            raise forms.ValidationError(message)
            
        

    class Meta:
        model = InfantArvProphylaxis
        fields = '__all__'


class ChildArvProphDatesForm(ChildModelFormMixin):
    class Meta:
        model = ChildArvProphDates
        fields = '__all__'
