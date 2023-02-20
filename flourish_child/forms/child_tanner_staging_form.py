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
            child_assents = ChildAssent.objects.filter(
                subject_identifier=subject_identifier)
            try:
                assent = child_assents.latest('consent_datetime')
            except ChildAssent.DoesNotExist:
                pass
            else:
                initial['child_gender'] = getattr(assent, 'gender')
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

        prev_instance = ChildTannerStaging.objects.filter(
            child_visit__appointment__subject_identifier=subject_identifier).order_by('-report_datetime').first()

        if prev_instance:
            self.initial['manarche_dt_avail'] = prev_instance.manarche_dt_avail
            self.initial['menarche_dt'] = prev_instance.menarche_dt
            self.initial['menarche_dt_est'] = prev_instance.menarche_dt_est
            self.initial['male_gen_stage'] = prev_instance.male_gen_stage
            self.initial['testclr_vol_measrd'] = prev_instance.testclr_vol_measrd

    class Meta:
        model = ChildTannerStaging
        fields = '__all__'
