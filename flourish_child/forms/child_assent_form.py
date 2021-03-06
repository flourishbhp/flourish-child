from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_child_validations.form_validators import ChildAssentFormValidator

from ..models import ChildAssent


class ChildAssentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = ChildAssentFormValidator

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            for key in self.fields.keys():
                self.fields[key].disabled = True

    class Meta:
        model = ChildAssent
        fields = '__all__'
