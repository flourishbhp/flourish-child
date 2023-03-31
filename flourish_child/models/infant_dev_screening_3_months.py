from django.db import models
from edc_constants.constants import YES

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import YES_NO_DONT_KNOW, HEARING_SPECIALISTS, VISION_SPECIALISTS, \
    COGNITIVE_SPECIALIST, MOTOR_SKILLS_SPECIALIST


class InfantDevScreening3Months(ChildCrfModelMixin):
    hearing = models.CharField(
        verbose_name='Startles to loud sounds',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
        )

    hearing_specialist = models.CharField(
        verbose_name=('Referred to any of the following specialists for hearing/'
                      'communication'),
        choices=HEARING_SPECIALISTS,
        max_length=15,
        default='No Referral'

        )

    vision = models.CharField(
        verbose_name='Follows face or close objects with eyes',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

        )

    vision_specialist = models.CharField(
        verbose_name=('Referred to any of the following specialists for Vision'
                      ' and adaptive'),
        choices=VISION_SPECIALISTS,
        max_length=30,
        default='No Referral'
        )

    cognitive_behavior = models.CharField(
        verbose_name='Smiles at people',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

        )

    cognitive_specialist = models.CharField(
        verbose_name=('Referred to any of the following specialists for'
                      ' Cognitive/Behavior'),
        choices=COGNITIVE_SPECIALIST,
        max_length=30,
        default='No Referral'
        )

    motor_skills_head = models.CharField(
        verbose_name='Holds head upright when held against shoulder',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

        )

    motor_skills_hands = models.CharField(
        verbose_name='Hands are open most of the time',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

        )

    motor_skills_specialist = models.CharField(
        verbose_name='Referred to any of the following specialists for Motor Skills',
        choices=MOTOR_SKILLS_SPECIALIST,
        max_length=30,
        default='No Referral'
        )

    caregiver_concerns = models.TextField(
        verbose_name='Caregiver concerns',
        null=True,
        blank=True
        )


    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Infant Developmental Screening for 3 Months'
        verbose_name_plural = 'Infant Developmental Screening for 3 Months'
