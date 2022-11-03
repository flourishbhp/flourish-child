from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import TbAdolAssentForm
from ..models import TbKnowledgeAdol
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(TbKnowledgeAdol, site=flourish_child_admin)
class TbKnowledgeAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = TbAdolAssentForm

    fieldsets = (
        (None, {
            'fields': [
                'report_datetime',
                'tb_informed',
                'tb_knowledge_medium',
                'tb_knowledge_medium_other', ]
        }),
        ("TB Knowledge Section (BELOW ARE QUESTIONS ABOUT KNOWLEDGE OF SYMPTOMS OF TB. "
         "FOR EACH QUESTION, PLEASE SAY 'YES' OR 'NO' OR 'I DON’T KNOW' OR 'PREFER NOT TO "
         "ANSWER')", {
             'fields': [
                 'fever_knowledge',
                 'cough_knowledge',
                 'night_sweats_knowledge',
                 'weight_loss_knowledge',
                 'rash_knowledge',
                 'headache_knowledge',
                 'vomiting_knowledge',
                 'body_ache_knowledge',
                 'other_knowledge']
         }),
        ('We will now move to the ways that a person can get TB.'
         ' For question, please answer as ‘yes’ or ‘no’ or ‘I '
         'do not know’ or ‘prefer not to answer’.', {
             'fields': [
                 'tb_utensils_transmit',
                 'tb_air_transmit',
                 'tb_treatable',
                 'tb_curable']
         }),
        ('TB Attitudes', {
            'fields': [
                'tb_community',
                'tb_community_treatment',
                'tb_community_treatment_other', ]
        }),
        audit_fieldset_tuple)

    radio_fields = {'tb_informed': admin.VERTICAL,
                    'fever_knowledge': admin.VERTICAL,
                    'cough_knowledge': admin.VERTICAL,
                    'night_sweats_knowledge': admin.VERTICAL,
                    'weight_loss_knowledge': admin.VERTICAL,
                    'rash_knowledge': admin.VERTICAL,
                    'headache_knowledge': admin.VERTICAL,
                    'vomiting_knowledge': admin.VERTICAL,
                    'body_ache_knowledge': admin.VERTICAL,
                    'tb_utensils_transmit': admin.VERTICAL,
                    'tb_air_transmit': admin.VERTICAL,
                    'tb_treatable': admin.VERTICAL,
                    'tb_curable': admin.VERTICAL, }

    filter_horizontal = ('tb_knowledge_medium',)
