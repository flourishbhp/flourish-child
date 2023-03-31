from flourish_child_validations.form_validators import ChildReferralFUFormValidator

from ..models import ChildGadPostReferral
from .child_form_mixin import ChildModelFormMixin


class ChildGadPostReferralForm(ChildModelFormMixin):

    form_validator_cls = ChildReferralFUFormValidator

    class Meta:
        model = ChildGadPostReferral
        fields = '__all__'
