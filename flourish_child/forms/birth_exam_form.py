from flourish_child_validations.form_validators import BirthExamFormValidator

from .child_form_mixin import ChildModelFormMixin
from ..models import BirthExam


class BirthExamForm(ChildModelFormMixin):

    form_validator_cls = BirthExamFormValidator

    class Meta:
        model = BirthExam
        fields = '__all__'
