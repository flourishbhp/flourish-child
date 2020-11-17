from ..models import AcademicPerformance
from .child_form_mixin import ChildModelFormMixin


class AcademicPerformanceForm(ChildModelFormMixin):

    class Meta:
        model = AcademicPerformance
        fields = '__all__'
