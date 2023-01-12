from django import forms
from flourish_child_validations.form_validators import HivKnowledgeFormValidator
from ..models import HivKnowledge
from .child_form_mixin import ChildModelFormMixin


class HivKnowledgeForm(ChildModelFormMixin):
    form_validator_cls = HivKnowledgeFormValidator

    class Meta:
        model = HivKnowledge
        fields = '__all__'
