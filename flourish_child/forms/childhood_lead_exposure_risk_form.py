from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models import ChildhoodLeadExposureRisk


class ChildhoodLeadExposureRiskForm(ChildModelFormMixin):
    class Meta:
        model = ChildhoodLeadExposureRisk
        fields = '__all__'
