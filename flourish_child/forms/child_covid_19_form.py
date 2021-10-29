from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from django import forms
from ..models import ChildCovid19
from flourish_form_validations.form_validators import Covid19FormValidator


class ChildCovid19Form(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = Covid19FormValidator

    class Meta:
        model = ChildCovid19
        fields = '__all__'
