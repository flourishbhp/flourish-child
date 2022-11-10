from flourish_child_validations.form_validators import ChildReferralFUFormValidator

from ..models import ChildPhqReferralFU
from .child_form_mixin import ChildModelFormMixin


class ChildPhqReferralFUForm(ChildModelFormMixin):

    form_validator_cls = ChildReferralFUFormValidator

    class Meta:
        model = ChildPhqReferralFU
        fields = '__all__'
