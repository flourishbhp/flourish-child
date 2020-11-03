from ..models import BirthData
from .child_form_mixin import ChildModelFormMixin


class BirthDataForm(ChildModelFormMixin):

    class Meta:
        model = BirthData
        fields = '__all__'
