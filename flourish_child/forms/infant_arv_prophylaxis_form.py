from django import forms
from edc_constants.constants import NO, YES

from flourish_child_validations.form_validators import ChildArvProphDatesFormValidator
from flourish_child_validations.form_validators import InfantArvProphylaxisFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import ChildArvProphDates, InfantArvProphylaxis


class InfantArvProphylaxisForm(ChildModelFormMixin):
    form_validator_cls = InfantArvProphylaxisFormValidator

    def clean(self):
        super().clean()

        took_art_proph = self.cleaned_data.get('took_art_proph', None)

        arvs_took_name = self.data.get('childarvprophdates_set-0-arv_name')

        child_arv_proph_dates_inlines_count = int(
            self.data.get('childarvprophdates_set-TOTAL_FORMS', 0))

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
    form_validator_cls = ChildArvProphDatesFormValidator

    def clean(self):
        super().clean()
        self.validate_arv_start_date_not_future()

    def has_changed(self):
        return True

    def validate_arv_start_date_not_future(self):
        arv_start_date = self.cleaned_data.get('arv_start_date')
        infant_arv_proph = self.cleaned_data.get('infant_arv_proph')
        if infant_arv_proph:
            report_datetime = infant_arv_proph.report_datetime.date()
            if arv_start_date > report_datetime:
                raise forms.ValidationError(
                    'The ARVs start date can not be after the Report date time'
                )

    class Meta:
        model = ChildArvProphDates
        fields = '__all__'
