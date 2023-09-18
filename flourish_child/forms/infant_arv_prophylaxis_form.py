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

    def clean(self):
        super().clean()
        stop_date = self.cleaned_data.get('arv_stop_date', None)
        infant_arv_proph = self.cleaned_data.get('infant_arv_proph', None)
        art_status = getattr(infant_arv_proph, 'art_status', None)
        if art_status == 'in_progress' and stop_date:
            message = {'arv_stop_date':
                       'ARV status is still in progress, do not provide stop date.'}
            raise forms.ValidationError(message)
        elif art_status in ['completed_in_time', 'completed_gt_28days'] and not stop_date:
            message = {'arv_stop_date':
                       'ARV status is completed, please provide stop date.'}
            raise forms.ValidationError(message)

    class Meta:
        model = ChildArvProphDates
        fields = '__all__'
