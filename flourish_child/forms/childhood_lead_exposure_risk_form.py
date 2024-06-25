from flourish_child.forms.child_form_mixin import ChildModelFormMixin
from flourish_child.models import ChildhoodLeadExposureRisk
from flourish_child_validations.form_validators.childhood_lead_exposure_risk_form_validator import \
    ChildhoodLeadExposureRiskFormValidator


class ChildhoodLeadExposureRiskForm(ChildModelFormMixin):
    form_validator_cls = ChildhoodLeadExposureRiskFormValidator
    class Meta:
        model = ChildhoodLeadExposureRisk
        fields = '__all__'
