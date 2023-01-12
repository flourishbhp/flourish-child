

from .child_form_mixin import ChildModelFormMixin
from ..models import TbLabResultsAdol


class TbLabResultsAdolForm(ChildModelFormMixin):

    class Meta:
        model = TbLabResultsAdol
        fields = '__all__'
