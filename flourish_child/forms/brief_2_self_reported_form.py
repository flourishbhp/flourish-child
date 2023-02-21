# from flourish_child_validations.form_validators import Brief2SelfReportedFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import Brief2SelfReported


class Brief2SelfReportedForm(ChildModelFormMixin):

#     form_validator_cls = Brief2SelfReportedFormValidator

    class Meta:
        model = Brief2SelfReported
        fields = '__all__'
