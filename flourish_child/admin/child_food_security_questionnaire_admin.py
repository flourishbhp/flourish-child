from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .model_admin_mixins import ChildCrfModelAdminMixin
from ..admin_site import flourish_child_admin
from ..forms import ChildFoodSecurityQuestionnaireForm
from ..models import ChildFoodSecurityQuestionnaire


@admin.register(ChildFoodSecurityQuestionnaire, site=flourish_child_admin)
class ChildFoodSecurityQuestionnaireAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = ChildFoodSecurityQuestionnaireForm

    instructions = None

    add_instructions = (
        '<p><b>***INSTRUCTIONS CLINIC STAFF: The questions about food security are part '
        'of our data collection efforts aimed at understanding various aspects of this '
        'critical issue. Your responses will help us gather valuable insights into '
        'the challenges people face regarding access to nutritious food and the '
        'factors influencing food security in different communities.<br/>It\'s '
        'important to note that your responses will be used solely for research and '
        'study purposes.We are not providing direct assistance or support based on '
        'the information you provide in these questions.Instead, the data collected '
        'will be analyzed to identify patterns, trends, and areas where '
        'interventions may be needed to improve food security outcomes.</b></p>')

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
    search_fields = ('how_often',)
    radio_fields = {"answerer": admin.VERTICAL,
                    "did_food_last": admin.VERTICAL,
                    "balanced_meals": admin.VERTICAL,
                    "cut_meals": admin.VERTICAL,
                    "how_often": admin.VERTICAL,
                    "eat_less": admin.VERTICAL,
                    "didnt_eat": admin.VERTICAL, }
