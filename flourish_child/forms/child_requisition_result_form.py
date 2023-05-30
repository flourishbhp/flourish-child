from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import ChildRequisitionResult


class ChildRequisitionResultForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = ChildRequisitionResult
        fields = '__all__'
