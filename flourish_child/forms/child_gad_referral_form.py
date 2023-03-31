from flourish_child_validations.form_validators import ChildReferralFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildGadReferral


class ChildGadReferralForm(ChildModelFormMixin):

    form_validator_cls = ChildReferralFormValidator

    class Meta:
        model = ChildGadReferral
        fields = '__all__'
