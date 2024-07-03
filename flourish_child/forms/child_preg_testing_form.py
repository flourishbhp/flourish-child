from django import forms
from django.apps import apps as django_apps
from edc_constants.constants import NO, NOT_APPLICABLE

from flourish_child_validations.form_validators import ChildPregTestingFormValidator
from .child_form_mixin import ChildModelFormMixin
from ..models import ChildPregTesting


class ChildPregTestingForm(ChildModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildPregTestingFormValidator

    @property
    def tanner_staging_model_cls(self):
        return django_apps.get_model('flourish_child.childtannerstaging')

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        previous_instance = getattr(self, 'previous_instance', None)
        initial = self.prefill_menarche_dates(initial, previous_instance)

        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

        if initial.get('menarche_start_dt', None):
            self.fields['menarche_start_dt'].widget = forms.DateInput(
                attrs={'readonly': 'readonly'})

        if initial.get('menarche_start_est', None):
            self.fields['menarche_start_est'].widget = forms.CharField(
                attrs={'readonly': 'readonly'})

        if initial.get('menarche', None):
            self.fields['menarche'].widget = forms.CharField(
                attrs={'readonly': 'readonly'})

    @property
    def menarche_fields(self):
        return ['menarche', 'menarche_start_dt', 'menarche_start_est']

    def prefill_menarche_dates(self, initial={}, prev_obj=None):
        key_map = {'menarche': 'manarche_dt_avail',
                   'menarche_start_dt': 'menarche_dt',
                   'menarche_start_est': 'menarche_dt_est'}

        for key in self.menarche_fields:
            tanner_staging = self.tanner_staging_model_cls.objects.filter(
                child_visit__subject_identifier=initial.get('subject_identifier', None))
            if tanner_staging.exists():
                tanner_staging_obj = tanner_staging.latest('report_datetime')
                if tanner_staging_obj.manarche_dt_avail not in ['not_reached',
                                                                NOT_APPLICABLE, NO]:
                    initial[key] = getattr(tanner_staging_obj, key_map.get(key, key),
                                           None)
            if prev_obj and not initial.get(key):
                initial[key] = getattr(prev_obj, key, None)
        return initial

    class Meta:
        model = ChildPregTesting
        fields = '__all__'
