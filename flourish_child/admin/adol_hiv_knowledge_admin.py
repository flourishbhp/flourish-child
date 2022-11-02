from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_child_admin
from ..forms import HivKnowledgeForm
from ..models import HivKnowledge
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(HivKnowledge, site=flourish_child_admin)
class HivKnowledgeAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):
    form = HivKnowledgeForm

    fieldsets = (
        (None, {
            'fields': [
                'report_datetime',
                'hiv_informed',
                'hiv_knowledge_medium',
                'hiv_knowledge_medium_other', ]
        }),
        ("HIV Knowledge Section (BELOW ARE QUESTIONS ABOUT KNOWLEDGE OF SYMPTOMS OF TB. "
         "FOR EACH QUESTION, PLEASE SAY 'YES' OR 'NO' OR 'I DON’T KNOW' OR 'PREFER NOT TO "
         "ANSWER')", {
             'fields': [
                 'fever_knowledge',
                 'cough_knowledge',
                 'night_sweats_knowledge',
                 'weight_loss_knowledge',
                 'rash_knowledge',
                 'headache_knowledge',
                 'other_knowledge']
         }),

        ('HIV Contraction Section', {
            'fields': [
                'hiv_utensils_transmit',
                'hiv_air_transmit',
                'hiv_sexual_transmit',
                'hiv_treatable',
                'hiv_curable']
        }),
        audit_fieldset_tuple)

    radio_fields = {'hiv_informed': admin.VERTICAL,
                    'fever_knowledge': admin.VERTICAL,
                    'cough_knowledge': admin.VERTICAL,
                    'night_sweats_knowledge': admin.VERTICAL,
                    'weight_loss_knowledge': admin.VERTICAL,
                    'rash_knowledge': admin.VERTICAL,
                    'headache_knowledge': admin.VERTICAL,
                    'hiv_utensils_transmit': admin.VERTICAL,
                    'hiv_air_transmit': admin.VERTICAL,
                    'hiv_sexual_transmit': admin.VERTICAL,
                    'hiv_treatable': admin.VERTICAL,
                    'hiv_curable': admin.VERTICAL, }

    filter_horizontal = ('hiv_knowledge_medium',)
