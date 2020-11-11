from ..models import ChildReferral
from .child_form_mixin import ChildModelFormMixin


class ChildReferralForm(ChildModelFormMixin):

    class Meta:
        model = ChildReferral
        fields = '__all__'
