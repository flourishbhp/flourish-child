from django import forms
# from flourish_form_validation.form_validators import HivKnowledgeFormValidator
from ..models import HivKnowledge
from .child_form_mixin import ChildModelFormMixin


class HivKnowledgeForm(ChildModelFormMixin):
    # form_validator_cls = HivKnowledgeFormValidator

    class Meta:
        model = HivKnowledge
        fields = '__all__'
