from django.db import models
from edc_constants.constants import YES

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import YES_NO_DONT_KNOW, HEARING_SPECIALISTS, VISION_SPECIALISTS, \
    COGNITIVE_SPECIALIST, MOTOR_SKILLS_SPECIALIST


class InfantDevScreening12Months(ChildCrfModelMixin):
    hearing = models.CharField(
        verbose_name='Uses simple gestures ',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    hearing_response = models.CharField(
        verbose_name=('Has one meaningful word (dada, mama) although sounds may not'
                      ' be clear'),
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    hearing_communication = models.CharField(
        verbose_name='Imitates different speech sounds',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    hearing_specialist = models.CharField(
        verbose_name=('Referred to any of the following specialists for hearing/'
                      'communication'),
        choices=HEARING_SPECIALISTS,
        max_length=15,
        default=''
    )

    eye_movement = models.CharField(
        verbose_name='Looks for toys/objects that disappear',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    familiar_obj = models.CharField(
        verbose_name='Looks closely at toys/objects and pictures',
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
        verbose_name='Imitates gestures (e.g., clapping hands)',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    understands = models.CharField(
        verbose_name='Understands ',
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

    stands = models.CharField(
        verbose_name='Stands with support',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    picks_objects = models.CharField(
        verbose_name='Picks up small objects with thumb and index finder',
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
        verbose_name = 'Infant Developmental Screening for 12 Months'
        verbose_name_plural = 'Infant Developmental Screening for 12 Months'
