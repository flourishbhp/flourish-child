from ..models import InfantFeedingPractices
from .child_form_mixin import ChildModelFormMixin


class InfantFeedingPracticesForm(ChildModelFormMixin):

    class Meta:
        model = InfantFeedingPractices
        fields = '__all__'
