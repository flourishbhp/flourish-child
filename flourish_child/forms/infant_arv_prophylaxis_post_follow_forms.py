from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models import InfantArvProphylaxisPostFollow
from flourish_child_validations.form_validators import \
    InfantArvProphylaxisPostFollowFormValidator


class InfantArvProphylaxisPostFollowForm(ChildModelFormMixin):
    form_validator_cls = InfantArvProphylaxisPostFollowFormValidator

    class Meta:
        model = InfantArvProphylaxisPostFollow
        fields = '__all__'
