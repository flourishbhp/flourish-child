from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ChildVisit


class ChildVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

#     form_validator_cls = MaternalVisitFormValidator

    class Meta:
        model = ChildVisit
        fields = '__all__'
