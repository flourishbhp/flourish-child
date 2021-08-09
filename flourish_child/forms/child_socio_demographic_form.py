from django import forms
from edc_constants.constants import YES, NO
from flourish_child_validations.form_validators import ChildSocioDemographicFormValidator

from ..models import ChildSocioDemographic
from .child_form_mixin import ChildModelFormMixin


class ChildSocioDemographicForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildSocioDemographicFormValidator

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance')
        previous_instance = getattr(self, 'previous_instance', None)

        if not instance and previous_instance:
            for key in self.base_fields.keys():
                if key not in ['child_visit', 'report_datetime']:
                    initial[key] = getattr(previous_instance, key)
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        previous_instance = getattr(self, 'previous_instance', None)
        has_changed = self.compare_instance_fields(previous_instance)
        med_history_changed = self.cleaned_data.get('med_history_changed')
        if med_history_changed:
            self.validate_med_history_changed(med_history_changed)
            if med_history_changed == YES and not has_changed:
                message = {'socio_demo_changed':
                           'Participant\'s Socio-demographic information has changed since '
                           'last visit. Please update the information on this form.'}
                raise forms.ValidationError(message)
            elif med_history_changed == NO and has_changed:
                message = {'med_history_changed':
                           'Participant\'s Socio-demographic information has not changed '
                           'since last visit. Please don\'t make any changes to this form.'}
                raise forms.ValidationError(message)
        cleaned_data = super().clean
        return cleaned_data

    class Meta:
        model = ChildSocioDemographic
        fields = '__all__'
