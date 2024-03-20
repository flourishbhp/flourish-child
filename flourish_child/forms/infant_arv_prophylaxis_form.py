from datetime import datetime

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

        self.validate_arv_start_date_not_future(child_arv_proph_dates_inlines_count)

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

    def validate_arv_start_date_not_future(self, inline_count):
        report_datetime = self.cleaned_data.get('report_datetime')
        report_datetime = report_datetime.date()
        for x in range(0, inline_count):
            arv_start_date = self.data.get(f'childarvprophdates_set-{x}-arv_start_date')
            if arv_start_date:
                arv_start_date = datetime.strptime(arv_start_date, '%Y-%m-%d').date()
                if arv_start_date > report_datetime:
                    raise forms.ValidationError(
                        'The ARVs start date can not be after the Report date time'
                    )

    class Meta:
        model = InfantArvProphylaxis
        fields = '__all__'


class ChildArvProphDatesForm(ChildModelFormMixin):
    form_validator_cls = ChildArvProphDatesFormValidator

    def has_changed(self):
        return True

    class Meta:
        model = ChildArvProphDates
        fields = '__all__'
