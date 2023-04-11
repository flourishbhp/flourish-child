from .child_form_mixin import ChildModelFormMixin
from ..models import ChildPhqDepressionScreening


class ChildPhqDepressionScreeningForm(ChildModelFormMixin):

    class Meta:
        model = ChildPhqDepressionScreening
        fields = '__all__'
