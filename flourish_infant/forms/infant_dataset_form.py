from django import forms
from edc_base.sites.forms import SiteModelFormMixin

from ..models import InfantDataset


class InfantDatasetForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = InfantDataset
        fields = '__all__'
