from flourish_child_validations.form_validators import (
    InfantCongenitalAnomaliesFormValidator, InfantFacialDefectFormValidator,
    InfantCleftDisorderFormFormValidator, InfantMouthUpGiFormValidator,
    InfantCardioDisorderFormValidator, InfantRespiratoryDefectFormValidator,
    InfantLowerGiFormValidator, InfantFemaleGenitalFormValidator,
    InfantMaleGenitalFormValidator, InfantRenalFormValidator,
    InfantMusculoskeletalFormValidator, InfantSkinFormValidator,
    InfantTrisomiesFormValidator, InfantCnsFormValidator)

from ..models import (InfantCongenitalAnomalies, InfantCardioDisorder,
                      InfantMusculoskeletal, InfantRenal, InfantFemaleGenital,
                      InfantCleftDisorder, InfantFacialDefect, InfantMouthUpGi,
                      InfantRespiratoryDefect, InfantLowerGi, InfantMaleGenital,
                      InfantSkin, InfantCns, InfantTrisomies)
from .child_form_mixin import ChildModelFormMixin


class InfantCongenitalAnomaliesForm(ChildModelFormMixin):

    form_validator_cls = InfantCongenitalAnomaliesFormValidator

    class Meta:
        model = InfantCongenitalAnomalies
        fields = '__all__'


class InfantFacialDefectForm(ChildModelFormMixin):

    form_validator_cls = InfantFacialDefectFormValidator

    class Meta:
        model = InfantFacialDefect
        fields = '__all__'


class InfantCleftDisorderForm(ChildModelFormMixin):

    form_validator_cls = InfantCleftDisorderFormFormValidator

    class Meta:
        model = InfantCleftDisorder
        fields = '__all__'


class InfantMouthUpGiForm(ChildModelFormMixin):

    form_validator_cls = InfantMouthUpGiFormValidator

    class Meta:
        model = InfantMouthUpGi
        fields = '__all__'


class InfantCardioDisorderForm(ChildModelFormMixin):

    form_validator_cls = InfantCardioDisorderFormValidator

    class Meta:
        model = InfantCardioDisorder
        fields = '__all__'


class InfantRespiratoryDefectForm(ChildModelFormMixin):

    form_validator_cls = InfantRespiratoryDefectFormValidator

    class Meta:
        model = InfantRespiratoryDefect
        fields = '__all__'


class InfantLowerGiForm(ChildModelFormMixin):

    form_validator_cls = InfantLowerGiFormValidator

    class Meta:
        model = InfantLowerGi
        fields = '__all__'


class InfantFemaleGenitalForm(ChildModelFormMixin):

    form_validator_cls = InfantFemaleGenitalFormValidator

    class Meta:
        model = InfantFemaleGenital
        fields = '__all__'


class InfantMaleGenitalForm(ChildModelFormMixin):

    form_validator_cls = InfantMaleGenitalFormValidator

    class Meta:
        model = InfantMaleGenital
        fields = '__all__'


class InfantRenalForm(ChildModelFormMixin):

    form_validator_cls = InfantRenalFormValidator

    class Meta:
        model = InfantRenal
        fields = '__all__'


class InfantMusculoskeletalForm(ChildModelFormMixin):

    form_validator_cls = InfantMusculoskeletalFormValidator

    class Meta:
        model = InfantMusculoskeletal
        fields = '__all__'


class InfantSkinForm(ChildModelFormMixin):

    form_validator_cls = InfantSkinFormValidator

    class Meta:
        model = InfantSkin
        fields = '__all__'


class InfantTrisomiesForm(ChildModelFormMixin):

    form_validator_cls = InfantTrisomiesFormValidator

    class Meta:
        model = InfantTrisomies
        fields = '__all__'


class InfantCnsForm(ChildModelFormMixin):

    form_validator_cls = InfantCnsFormValidator

    class Meta:
        model = InfantCns
        fields = '__all__'
