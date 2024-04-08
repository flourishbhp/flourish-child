from django import forms
from django.apps import apps as django_apps
from django.db.models import ManyToManyField, DateField, DateTimeField, IntegerField
from edc_constants.constants import YES, NO
from itertools import chain

from ..models import InfantFeeding
from .child_form_mixin import ChildModelFormMixin
from flourish_child_validations.form_validators import InfantFeedingFormValidator


class InfantFeedingForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = InfantFeedingFormValidator
    birth_feeding_and_vaccine_model = 'flourish_child.birthfeedingvaccine'

    @property
    def birth_feeding_and_vaccine_model_cls(self):
        return django_apps.get_model(self.birth_feeding_and_vaccine_model)

    last_att_sche_visit = forms.DateField(
        label='The last infant feeding form was completed on ',
        widget=forms.DateInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):

        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance')
        previous_instance = getattr(self, 'previous_instance', None)
        prev_feeding_completed = getattr(
            previous_instance, 'formula_feedng_completd', None)
        dt_formula_introduced = getattr(
            previous_instance, 'dt_formula_introduced', None)

        if not instance and previous_instance:
            initial['last_att_sche_visit'] = getattr(
                previous_instance, 'report_datetime').date()

            for key in self.base_fields.keys():

                if key == 'dt_formula_introduced' and prev_feeding_completed == YES:
                    initial[key] = dt_formula_introduced
                    continue
                if key in ['solid_foods', 'solid_foods_past_week']:
                    key_manager = getattr(previous_instance, key)
                    initial[key] = [obj.id for obj in key_manager.all()]
                    continue
                if key not in ['child_visit', 'report_datetime', 'infant_feeding_changed',
                               'last_att_sche_visit', 'solid_foods_past_week', 'grain_intake_freq',
                               'legumes_intake_freq', 'dairy_intake_freq', 'flesh_foods_freq',
                               'eggs_intake_freq', 'porridge_intake_freq', 'vitamin_a_fruits_freq',
                               'other_fruits_vegies', 'other_fruits_freq', 'other_solids',
                               'other_solids_freq']:
                    initial[key] = getattr(previous_instance, key)

        subject_identifier = initial.get('subject_identifier', None)
        for key in ['bf_start_dt', 'bf_start_dt_est', 'dt_formula_introduced', 'dt_formula_est']:
            key_value, _exists = self.prefill_bf_dates(key, subject_identifier)
            if _exists:
                initial[key] = key_value
                continue
        kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

        # Make breasfeeding start fields readonly if auto-filled from previous visit
        if initial.get('bf_start_dt', None) and previous_instance != None:
            self.fields['ever_breastfed'].widget = forms.TextInput(
                attrs={'readonly': 'readonly'})
            self.fields['bf_start_dt_est'].widget = forms.TextInput(
                attrs={'readonly': 'readonly'})
            self.fields['bf_start_dt'].widget = forms.DateInput(
                attrs={'readonly': 'readonly'})

        if (initial.get('dt_weaned', None) and
                initial.get('child_weaned', None) == YES):
            self.fields['child_weaned'].widget = forms.TextInput(
                attrs={'readonly': 'readonly'})
            self.fields['dt_weaned'].widget = forms.DateInput(
                attrs={'readonly': 'readonly'})
        if initial.get('dt_formula_introduced', None):
            self.fields['dt_formula_introduced'].widget = forms.DateInput(
                attrs={'readonly': 'readonly'})
        if initial.get('solid_foods_dt', None):
            self.fields['solid_foods_dt'].widget = forms.DateInput(
                attrs={'readonly': 'readonly'})

    def clean(self):
        previous_instance = getattr(self, 'previous_instance', None)
        has_changed = self.compare_instance_fields(
            prev_instance=previous_instance)
        feeding_changed = self.cleaned_data.get('infant_feeding_changed')
        if feeding_changed == YES and not has_changed:
            message = {'infant_feeding_changed':
                       'Participant\'s infant feeding information has changed '
                       'since last visit. Please update the information on this form.'}
            raise forms.ValidationError(message)
        elif feeding_changed == NO and has_changed:
            message = {'infant_feeding_changed':
                       'Participant\'s infant feeding information has not changed '
                       'since last visit. Please don\'t make any changes to this form.'}
            raise forms.ValidationError(message)
        form_validator = self.form_validator_cls(
            cleaned_data=self.cleaned_data)
        cleaned_data = form_validator.validate()
        return cleaned_data

    def compare_instance_fields(self, prev_instance=None):
        exclude_fields = ['modified', 'created', 'user_created', 'user_modified',
                          'hostname_created', 'hostname_modified', 'device_created',
                          'device_modified', 'report_datetime', 'child_visit',
                          'infant_feeding_changed', 'last_att_sche_visit', ]
        m2m_fields = ['solid_foods', 'solid_foods_past_week']
        if prev_instance:
            other_values = self.model_to_dict(
                prev_instance, exclude=exclude_fields)
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
                data[f.name] = [str(obj.id)
                                for obj in f.value_from_object(instance)]
                continue
            if isinstance(f, (DateTimeField, DateField, IntegerField)):
                if f.value_from_object(instance) is not None:
                    data[f.name] = f.value_from_object(instance).__str__()
                continue
            data[f.name] = f.value_from_object(instance) or None
        return data

    def prefill_bf_dates(self, key=None, subject_identifier=None):
        key_map = {'bf_start_dt': 'breastfeed_start_dt',
                   'bf_start_dt_est': 'breastfeed_start_est',
                   'dt_formula_introduced': 'formulafeed_start_dt',
                   'dt_formula_est': 'formulafeed_start_est'}

        feeding_n_vaccine_objs = self.birth_feeding_and_vaccine_model_cls.objects.filter(
            child_visit__subject_identifier=subject_identifier)
        key_value = None
        if feeding_n_vaccine_objs.exists():
            feeding_n_vaccine_obj = feeding_n_vaccine_objs.latest(
                'report_datetime')
            key_value = getattr(feeding_n_vaccine_obj,
                                key_map.get(key, key), None)

        return (key_value, True) if key_value else (key_value, False)

    class Meta:
        model = InfantFeeding
        fields = '__all__'
