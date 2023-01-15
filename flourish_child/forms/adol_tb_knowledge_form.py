from django import forms
from flourish_child_validations.form_validators import TbKnowledgeFormValidator
from ..models import TbKnowledgeAdol
from .child_form_mixin import ChildModelFormMixin


class TbKnowledgeAdolForm(ChildModelFormMixin):
    form_validator_cls = TbKnowledgeFormValidator

    class Meta:
        model = TbKnowledgeAdol
        fields = '__all__'
