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
        ('HIV Knowledge', {
            'fields': [
                'child_visit',
                'report_datetime',
                'hiv_informed',
                'hiv_knowledge_medium',
                'hiv_knowledge_medium_other', ]
        }),
        ("We will now move to recognizing signs and symptoms of HIV. "
         "For each symptom or sign I say, please answer as 'yes' or 'no' or 'I do not know' "
         "or 'prefer not to answer'", {
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

        ('We will now move to the ways that a person can get HIV.'
         ' For question, please answer as ‘yes’ or ‘no’ or ‘I '
         'do not know’ or ‘prefer not to answer’.', {
             'fields': [
                 'hiv_utensils_transmit',
                 'hiv_air_transmit',
                 'protected_sexual_transmit',
                 'unprotected_sexual_transmit',
                 'hiv_treatable',
                 'hiv_curable']
         }),

        ('HIV Attitudes', {
            'fields': [
                'hiv_community',
                'hiv_community_treatment',
                'hiv_community_treatment_other']
        }),
        audit_fieldset_tuple)

    radio_fields = {'hiv_informed': admin.VERTICAL,
                    'fever_knowledge': admin.VERTICAL,
                    'cough_knowledge': admin.VERTICAL,
                    'night_sweats_knowledge': admin.VERTICAL,
                    'weight_loss_knowledge': admin.VERTICAL,
                    'rash_knowledge': admin.VERTICAL,
                    'headache_knowledge': admin.VERTICAL,
                    'vomiting_knowledge': admin.VERTICAL,
                    'body_ache_knowledge': admin.VERTICAL,
                    'hiv_utensils_transmit': admin.VERTICAL,
                    'hiv_air_transmit': admin.VERTICAL,
                    'protected_sexual_transmit': admin.VERTICAL,
                    'unprotected_sexual_transmit': admin.VERTICAL,
                    'hiv_treatable': admin.VERTICAL,
                    'hiv_community': admin.VERTICAL,
                    'hiv_community_treatment': admin.VERTICAL,
                    'hiv_curable': admin.VERTICAL,}

    filter_horizontal = ('hiv_knowledge_medium',)
