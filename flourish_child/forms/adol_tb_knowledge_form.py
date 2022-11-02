from django import forms
# from flourish_form_validation.form_validators import TbKnowledgeAdolFormValidator
from ..models import TbKnowledgeAdol
from .child_form_mixin import ChildModelFormMixin


class TbKnowledgeAdolForm(ChildModelFormMixin):
    # form_validator_cls = TbKnowledgeAdolFormValidator

    class Meta:
        model = TbKnowledgeAdol
        fields = '__all__'
