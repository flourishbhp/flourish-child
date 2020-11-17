from .child_form_mixin import ChildModelFormMixin
from ..models import BirthExam


class BirthExamForm(ChildModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = BirthExam
        fields = '__all__'
