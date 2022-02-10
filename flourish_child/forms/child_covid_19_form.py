from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from django import forms
from ..models import ChildCovid19
from flourish_form_validations.form_validators import Covid19FormValidator


class ChildCovid19Form(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = Covid19FormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        subject_identifier = self.initial.get('subject_identifier', None)

        if not subject_identifier:
            return

        prev_instance = ChildCovid19.objects \
            .filter(child_visit__appointment__subject_identifier=subject_identifier) \
            .order_by('-report_datetime') \
            .first()

        if prev_instance:
            self.initial['fully_vaccinated'] = prev_instance.fully_vaccinated
            self.initial['vaccination_type'] = prev_instance.vaccination_type
            self.initial['other_vaccination_type'] = prev_instance.other_vaccination_type
            self.initial['first_dose'] = prev_instance.first_dose
            self.initial['second_dose'] = prev_instance.second_dose

    class Meta:
        model = ChildCovid19
        fields = '__all__'
