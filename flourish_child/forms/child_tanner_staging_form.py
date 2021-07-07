from django import forms
from flourish_child_validations.form_validators import ChildTannerStagingFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildTannerStaging, ChildAssent


class ChildTannerStagingForm(ChildModelFormMixin, forms.ModelForm):

    form_validator_cls = ChildTannerStagingFormValidator

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        subject_identifier = initial.get('subject_identifier')
        if subject_identifier:
            try:
                assent = ChildAssent.objects.get(
                    subject_identifier=subject_identifier)
            except ChildAssent.DoesNotExist:
                pass
            else:
                initial['child_gender'] = getattr(assent, 'gender')
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    class Meta:
        model = ChildTannerStaging
        fields = '__all__'
