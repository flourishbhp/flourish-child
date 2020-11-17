from ..models import (InfantCongenitalAnomalies, InfantCardioDisorder,
                      InfantMusculoskeletal, InfantRenal, InfantFemaleGenital,
                      InfantCleftDisorder, InfantFacialDefect, InfantMouthUpGi,
                      InfantRespiratoryDefect, InfantLowerGi, InfantMaleGenital,
                      InfantSkin, InfantCns, InfantTrisomies)
from .child_form_mixin import ChildModelFormMixin


class InfantCongenitalAnomaliesForm(ChildModelFormMixin):

    class Meta:
        model = InfantCongenitalAnomalies
        fields = '__all__'


class InfantFacialDefectForm(ChildModelFormMixin):

    class Meta:
        model = InfantFacialDefect
        fields = '__all__'


class InfantCleftDisorderForm(ChildModelFormMixin):

    class Meta:
        model = InfantCleftDisorder
        fields = '__all__'


class InfantMouthUpGiForm(ChildModelFormMixin):

    class Meta:
        model = InfantMouthUpGi
        fields = '__all__'


class InfantCardioDisorderForm(ChildModelFormMixin):

    class Meta:
        model = InfantCardioDisorder
        fields = '__all__'


class InfantRespiratoryDefectForm(ChildModelFormMixin):

    class Meta:
        model = InfantRespiratoryDefect
        fields = '__all__'


class InfantLowerGiForm(ChildModelFormMixin):

    class Meta:
        model = InfantLowerGi
        fields = '__all__'


class InfantFemaleGenitalForm(ChildModelFormMixin):

    class Meta:
        model = InfantFemaleGenital
        fields = '__all__'


class InfantMaleGenitalForm(ChildModelFormMixin):

    class Meta:
        model = InfantMaleGenital
        fields = '__all__'


class InfantRenalForm(ChildModelFormMixin):

    class Meta:
        model = InfantRenal
        fields = '__all__'


class InfantMusculoskeletalForm(ChildModelFormMixin):

    class Meta:
        model = InfantMusculoskeletal
        fields = '__all__'


class InfantSkinForm(ChildModelFormMixin):

    class Meta:
        model = InfantSkin
        fields = '__all__'


class InfantTrisomiesForm(ChildModelFormMixin):

    class Meta:
        model = InfantTrisomies
        fields = '__all__'


class InfantCnsForm(ChildModelFormMixin):

    class Meta:
        model = InfantCns
        fields = '__all__'
