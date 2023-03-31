from django.db import models
from edc_constants.constants import YES

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import YES_NO_DONT_KNOW, HEARING_SPECIALISTS, VISION_SPECIALISTS, \
    COGNITIVE_SPECIALIST, MOTOR_SKILLS_SPECIALIST


class InfantDevScreening9Months(ChildCrfModelMixin):
    speaking = models.CharField(
        verbose_name='Babbles (‘ma-ma’, ‘da-da’)',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    hearing = models.CharField(
        verbose_name='Turns when called',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    speaking_specialist = models.CharField(
        verbose_name=('Referred to any of the following specialists for hearing/'
                      'communication'),
        choices=HEARING_SPECIALISTS,
        max_length=15,
        default=''
    )

    vision = models.CharField(
        verbose_name='Eyes focus on far objects',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    vision_specialist = models.CharField(
        verbose_name=('Referred to any of the following specialists for Vision'
                      ' and adaptive'),
        choices=VISION_SPECIALISTS,
        max_length=30,
        default=''
    )

    cognitive_behavior = models.CharField(
        verbose_name='Throws, bands toys/objects',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    cognitive_behavior_reactions = models.CharField(
        verbose_name='Reacts when caregiver leaves, calms when she/he returns',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    cognitive_specialist = models.CharField(
        verbose_name=('Referred to any of the following specialists for'
                      ' Cognitive/Behavior'),
        choices=COGNITIVE_SPECIALIST,
        max_length=30,
        default=''
    )

    sits = models.CharField(
        verbose_name='Sits without support',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    moves_objects = models.CharField(
        verbose_name='Moves object from hand to hand',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    motor_skills_specialist = models.CharField(
        verbose_name='Referred to any of the following specialists for Motor Skills',
        choices=MOTOR_SKILLS_SPECIALIST,
        max_length=30,
        default=''
    )

    caregiver_concerns = models.TextField(
        verbose_name='Caregiver concerns',
        null=True,
        blank=True
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant Developmental Screening for 9 Months'
        verbose_name_plural = 'Infant Developmental Screening for 9 Months'
