from ..models import ChildReferral
from .child_form_mixin import ChildModelFormMixin

from flourish_child_validations.form_validators import ChildReferralFormValidator


class ChildReferralForm(ChildModelFormMixin):

    form_validator_cls = ChildReferralFormValidator

    class Meta:
        model = ChildReferral
        fields = '__all__'
