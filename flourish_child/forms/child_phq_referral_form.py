from flourish_child_validations.form_validators import ChildReferralFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildPhqReferral


class ChildPhqReferralForm(ChildModelFormMixin):

    form_validator_cls = ChildReferralFormValidator

    class Meta:
        model = ChildPhqReferral
        fields = '__all__'
