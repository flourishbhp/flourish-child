from django import forms
from django.db.models import ManyToManyField

from edc_constants.constants import YES, NO, NOT_APPLICABLE
from flourish_child_validations.form_validators import ChildMedicalHistoryFormValidator
from itertools import chain

from ..models import ChildMedicalHistory
from .child_form_mixin import ChildModelFormMixin


class ChildMedicalHistoryForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildMedicalHistoryFormValidator

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance')
        previous_instance = getattr(self, 'previous_instance', None)
        if not instance and previous_instance:
            for key in self.base_fields.keys():
                if key in ['child_chronic', ]:
                    key_manager = getattr(previous_instance, key)
                    initial[key] = [obj.id for obj in key_manager.all()]
                    continue
                if key not in ['child_visit', 'report_datetime']:
                    initial[key] = getattr(previous_instance, key)
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        previous_instance = getattr(self, 'previous_instance', None)
        has_changed = self.compare_instance_fields(previous_instance)
        med_history_changed = cleaned_data.get('med_history_changed')
        if med_history_changed:
            self.validate_med_history_changed(med_history_changed)
            if med_history_changed == YES and not has_changed:
                message = {'med_history_changed':
                           'Participant\'s medical history has changed since last '
                           'visit. Please update the information on this form.'}
                raise forms.ValidationError(message)
            elif med_history_changed == NO and has_changed:
                message = {'med_history_changed':
                           'Participant\'s medical history has not changed since '
                           'last visit. Please don\'t make any changes to this form.'}
                raise forms.ValidationError(message)
        return cleaned_data

    def validate_med_history_changed(self, med_history_changed):
        if med_history_changed == NOT_APPLICABLE:
            msg = {'med_history_changed': 'This field is applicable.'}
            raise forms.ValidationError(msg)

    def compare_instance_fields(self, prev_instance=None):
        exclude_fields = ['modified', 'created', 'user_created', 'user_modified',
                          'hostname_created', 'hostname_modified', 'device_created',
                          'device_modified', 'report_datetime', 'child_visit',
                          'med_history_changed', ]
        m2m_fields = ['child_chronic', ]
        if prev_instance:
            other_values = self.model_to_dict(prev_instance, exclude=exclude_fields)
            values = {key: self.data.get(key) or None if key not in m2m_fields else
                      self.data.getlist(key) for key in other_values.keys()}
            return values != other_values
        return False

    def model_to_dict(self, instance, exclude):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if not getattr(f, 'editable', False):
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                data[f.name] = [str(obj.id) for obj in f.value_from_object(instance)]
                continue
            data[f.name] = f.value_from_object(instance) or None
        return data

    class Meta:
        model = ChildMedicalHistory
        fields = '__all__'
