from django import forms
from flourish_child_validations.form_validators import ChildTannerStagingFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildTannerStaging


class ChildTannerStagingForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildTannerStagingFormValidator

    class Meta:
        model = ChildTannerStaging
        fields = '__all__'
