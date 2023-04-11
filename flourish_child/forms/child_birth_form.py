from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from flourish_child_validations.form_validators import ChildBirthFormValidator

from ..models import ChildBirth


class ChildBirthForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ChildBirthFormValidator

    class Meta:
        model = ChildBirth
        fields = '__all__'
