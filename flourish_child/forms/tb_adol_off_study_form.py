from django import forms

from flourish_child.models import TBAdolOffStudy
from flourish_prn.forms import ChildOffStudyForm


class TBAdolOffStudyForm(ChildOffStudyForm, forms.ModelForm):
    class Meta:
        model = TBAdolOffStudy
        fields = '__all__'
