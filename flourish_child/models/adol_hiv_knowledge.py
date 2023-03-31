from django.db import models


from ..choices import YES_NO_PNTA, YES_NO_DN_PNTA, COMMUNITY_IMPACT, COMMUNITY_TREATMENT
from .list_models import HIVKnowledgeMedium
from .child_crf_model_mixin import ChildCrfModelMixin


class HivKnowledge(ChildCrfModelMixin):
    hiv_informed = models.CharField(
        verbose_name='Do you feel well-informed about HIV?',
        choices=YES_NO_PNTA,
        max_length=15)

    hiv_knowledge_medium = models.ManyToManyField(
        HIVKnowledgeMedium,
        verbose_name='Where did you first learn about HIV?')

    hiv_knowledge_medium_other = models.TextField(
        verbose_name='If other, specify',
        max_length=150,
        blank=True,
        null=True)

    fever_knowledge = models.CharField(
        verbose_name='Fever?',
        choices=YES_NO_DN_PNTA,
        max_length=30, )

    cough_knowledge = models.CharField(
        verbose_name='Cough?',
        choices=YES_NO_DN_PNTA,
        max_length=30, )

    night_sweats_knowledge = models.CharField(
        verbose_name='Night Sweats?',
        choices=YES_NO_DN_PNTA,
        max_length=30, )

    weight_loss_knowledge = models.CharField(
        verbose_name='Weight Loss?',
        choices=YES_NO_DN_PNTA,
        max_length=30, )

    rash_knowledge = models.CharField(
        verbose_name='Rash?',
        choices=YES_NO_DN_PNTA,
        max_length=30, )

    headache_knowledge = models.CharField(
        verbose_name='Headache?',
        choices=YES_NO_DN_PNTA,
        max_length=30, )

    vomiting_knowledge = models.CharField(
        verbose_name='Vomiting?',
        choices=YES_NO_DN_PNTA,
        max_length=30, )

    body_ache_knowledge = models.CharField(
        verbose_name='Body ache?',
        choices=YES_NO_DN_PNTA,
        max_length=30, )

    other_knowledge = models.TextField(
        verbose_name='Other: (free text)',
        max_length=150,
        blank=True,
        null=True)

    hiv_utensils_transmit = models.CharField(
        verbose_name='Can a person get HIV by sharing dishes, plates, cups, and spoons?',
        choices=YES_NO_DN_PNTA,
        max_length=25, )

    hiv_air_transmit = models.CharField(
        verbose_name='Can a person get HIV through the air when a person with TB coughs?',
        choices=YES_NO_DN_PNTA,
        max_length=25, )

    protected_sexual_transmit = models.CharField(
        verbose_name='Can a person get HIV when having protected sex with another person?',
        choices=YES_NO_DN_PNTA,
        max_length=25, )

    unprotected_sexual_transmit = models.CharField(
        verbose_name='Can a person get HIV when having unprotected sex with another person?',
        choices=YES_NO_DN_PNTA,
        max_length=25, )

    hiv_sexual_transmit_other = models.TextField(
        verbose_name="Other (free text)"
    )

    hiv_treatable = models.CharField(
        verbose_name='Can HIV be treated? ',
        choices=YES_NO_DN_PNTA,
        max_length=25, )

    hiv_curable = models.CharField(
        verbose_name='Can HIV be cured? ',
        choices=YES_NO_DN_PNTA,
        max_length=25, )

    hiv_community = models.CharField(
        verbose_name='How would you rate HIV as a problem in your community?',
        choices=COMMUNITY_IMPACT,
        max_length=60, )

    hiv_community_treatment = models.CharField(
        verbose_name='In your community, how is a person who has HIV usually'
                     ' regarded/treated by other people in the community?',
        choices=COMMUNITY_TREATMENT,
        max_length=60, )

    hiv_community_treatment_other = models.TextField(
        verbose_name='Other (free text)',
        blank=True,
        null=True
    )

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Knowledge and attitudes for HIV'
        verbose_name_plural = 'Knowledge and attitudes for HIV'
