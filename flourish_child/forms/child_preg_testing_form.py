from django import forms
from django.apps import apps as django_apps

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
        instance = kwargs.get('instance')
        if not instance:
            for key in self.base_fields.keys():
                if key in ['menarche', 'menarche_start_dt', 'menarche_start_est']:
                    initial, _exists = self.prefill_menarche_dates(key, initial)
                    if _exists:
                        continue

        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

        if initial.get('menarche_start_dt', None):
            self.fields['menarche_start_dt'].widget = forms.DateInput(
                attrs={'readonly': 'readonly'})

    def prefill_menarche_dates(self, key=None, initial={}):
        key_map = {'menarche': 'manarche_dt_avail',
                   'menarche_start_dt': 'menarche_dt',
                   'menarche_start_est': 'menarche_dt_est'}

        tanner_staging = self.tanner_staging_model_cls.objects.filter(
            child_visit__subject_identifier=initial.get('subject_identifier', None))
        key_value = None
        if tanner_staging.exists():
            tanner_staging_obj = tanner_staging.latest('report_datetime')
            key_value = getattr(tanner_staging_obj, key_map.get(key, key), None)
        initial[key] = key_value
        return (initial, True) if key_value else (initial, False)

    class Meta:
        model = ChildPregTesting
        fields = '__all__'
