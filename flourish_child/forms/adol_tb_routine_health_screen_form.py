from django import forms
from django.core.exceptions import ValidationError
# from flourish_form_validation.form_validators import TbRoutineScreenAdolescentFormValidator
from ..models import TbRoutineScreenAdol, TbHealthVisitAdol
from .child_form_mixin import ChildModelFormMixin, InlineChildModelFormMixin
from flourish_child_validations.form_validators import TbScreeningDuringEncountersFormValidator

class TbRoutineScreenAdolForm(ChildModelFormMixin):
    # form_validator_cls = TbScreeningDuringEncountersFormValidator
    
    
    def clean(self):
        
        clean_data = super().clean()
        
        tb_healthvisit_inlines =  int(self.data.get('tbhealthvisitadol_set-TOTAL_FORMS', 0))
        
        try:
            tb_health_visits_counter = int(clean_data.get('tb_health_visits'))
        except ValueError:
            pass
        else:
            if tb_healthvisit_inlines != tb_health_visits_counter:
                raise ValidationError({'tb_health_visits': 'Not equal to the provided number of visits'})
            
        return clean_data

    class Meta:
        model = TbRoutineScreenAdol
        fields = '__all__'



class TbHealthVisitAdolForm(InlineChildModelFormMixin):
    form_validator_cls = TbScreeningDuringEncountersFormValidator    
    class Meta:
        model = TbHealthVisitAdol
        fields = '__all__'
        
