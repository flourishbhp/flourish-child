from ..models import ChildSocioDemographic
from .child_form_mixin import ChildModelFormMixin


class ChildSocioDemographicForm(ChildModelFormMixin):

    class Meta:
        model = ChildSocioDemographic
        fields = '__all__'
