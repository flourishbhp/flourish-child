from flourish_child_validations.form_validators import \
    ChildPerformanceFormValidator
from ..models import AcademicPerformance
from .child_form_mixin import ChildModelFormMixin


class AcademicPerformanceForm(ChildModelFormMixin):

    form_validator_cls = ChildPerformanceFormValidator

    class Meta:
        model = AcademicPerformance
        fields = '__all__'
