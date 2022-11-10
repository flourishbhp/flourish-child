from flourish_child_validations.form_validators import ChildReferralFUFormValidator

from ..models import ChildGadReferralFU
from .child_form_mixin import ChildModelFormMixin


class ChildGadReferralFUForm(ChildModelFormMixin):

    form_validator_cls = ChildReferralFUFormValidator

    class Meta:
        model = ChildGadReferralFU
        fields = '__all__'
