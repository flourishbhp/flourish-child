from django import forms
from edc_base.sites.forms import SiteModelFormMixin

from ..models import ChildDataset


class ChildDatasetForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildDataset
        fields = '__all__'
