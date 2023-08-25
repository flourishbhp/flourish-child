from flourish_child_validations.form_validators import TbReferralAdolFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import TbReferalAdol


class TbReferralAdolForm(ChildModelFormMixin):

    form_validator_cls = TbReferralAdolFormValidator

    class Meta:
        model = TbReferalAdol
        fields = '__all__'
