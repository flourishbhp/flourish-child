from flourish_child_validations.form_validators import ChildReferralFUFormValidator

from ..models import ChildPhqPostReferral
from .child_form_mixin import ChildModelFormMixin


class ChildPhqPostReferralForm(ChildModelFormMixin):

    form_validator_cls = ChildReferralFUFormValidator

    class Meta:
        model = ChildPhqPostReferral
        fields = '__all__'
