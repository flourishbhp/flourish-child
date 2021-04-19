from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_child_validations.form_validators import ChildVisitFormValidator
from ..models import ChildVisit


class ChildVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ChildVisitFormValidator

    class Meta:
        model = ChildVisit
        fields = '__all__'
