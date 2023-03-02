# from flourish_child_validations.form_validators import Brief2ParentFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import Brief2Parent


class Brief2ParentForm(ChildModelFormMixin):

#     form_validator_cls = Brief2ParentFormValidator

    class Meta:
        model = Brief2Parent
        fields = '__all__'
