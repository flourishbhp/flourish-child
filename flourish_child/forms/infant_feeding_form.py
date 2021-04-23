from ..models import InfantFeeding
from .child_form_mixin import ChildModelFormMixin


class InfantFeedingForm(ChildModelFormMixin):

    class Meta:
        model = InfantFeeding
        fields = '__all__'
