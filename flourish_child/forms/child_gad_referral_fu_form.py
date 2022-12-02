from flourish_child_validations.form_validators import ChildReferralFUFormValidator

from ..models import ChildGadReferralFU
from .child_form_mixin import ChildModelFormMixin


class ChildGadReferralFUForm(ChildModelFormMixin):

    form_validator_cls = ChildReferralFUFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['emo_support_type'].label = ('4. What kind of emotional support are you '
                                                 'receiving?')

    class Meta:
        model = ChildGadReferralFU
        fields = '__all__'
