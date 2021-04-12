from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import ChildFoodSecurityQuestionnaireForm
from ..models import ChildFoodSecurityQuestionnaire
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(ChildFoodSecurityQuestionnaire, site=flourish_child_admin)
class ChildFoodSecurityQuestionnaireAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = ChildFoodSecurityQuestionnaireForm

    instructions = ('Please state for participant “I’m going to read you '
                    'several statements that people have made about their food'
                    ' situation. For these statements, please tell me whether'
                    ' the statement was often true, sometimes true, or never '
                    'true for (you/your household) in the last 12 months—that '
                    'is, since last (name of current month).”')

    fieldsets = (
        (None, {
            'fields': [
                'child_visit',
                'report_datetime',
                'answerer',
                'did_food_last',
                'balanced_meals',
                'cut_meals',
                'how_often',
                'eat_less',
                'didnt_eat']}
         ), audit_fieldset_tuple)

    list_display = ('child_visit',
                    'answerer',
                    'how_often')
    list_filter = ('report_datetime', 'how_often')
    search_fields = ('how_often', )
    radio_fields = {"answerer": admin.VERTICAL,
                    "did_food_last": admin.VERTICAL,
                    "balanced_meals": admin.VERTICAL,
                    "cut_meals": admin.VERTICAL,
                    "how_often": admin.VERTICAL,
                    "eat_less": admin.VERTICAL,
                    "didnt_eat": admin.VERTICAL,}
