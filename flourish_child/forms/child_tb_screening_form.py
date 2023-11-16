from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models.child_tb_screening import ChildTBScreening
from flourish_child_validations.form_validators.child_tb_screening_form_validator import \
    ChildTBScreeningFormValidator


class ChildTBScreeningForm(ChildModelFormMixin):
    form_validator_cls = ChildTBScreeningFormValidator

    class Meta:
        model = ChildTBScreening
        fields = '__all__'
