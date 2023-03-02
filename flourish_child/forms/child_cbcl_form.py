# from flourish_child_validations.form_validators import Brief2ParentFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildCBCL


class ChildCBCLForm(ChildModelFormMixin):

#     form_validator_cls = Brief2ParentFormValidator

    class Meta:
        model = ChildCBCL
        fields = '__all__'
