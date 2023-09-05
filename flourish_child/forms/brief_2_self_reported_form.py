from flourish_child_validations.form_validators.brief_2_forms_validators import \
    Brief2SelfReportedFormsValidators
from .child_form_mixin import ChildModelFormMixin
from ..models import Brief2SelfReported


class Brief2SelfReportedForm(ChildModelFormMixin):
    form_validator_cls = Brief2SelfReportedFormsValidators

    class Meta:
        model = Brief2SelfReported
        fields = '__all__'
