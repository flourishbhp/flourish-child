from flourish_child_validations.form_validators import ChildPennCNBFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import ChildPennCNB


class ChildPennCNBForm(ChildModelFormMixin):

    form_validator_cls = ChildPennCNBFormValidator

    class Meta:
        model = ChildPennCNB
        fields = '__all__'
