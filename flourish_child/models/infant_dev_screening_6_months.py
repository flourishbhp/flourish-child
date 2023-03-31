from django.db import models
from edc_constants.constants import YES

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import YES_NO_DONT_KNOW, HEARING_SPECIALISTS, VISION_SPECIALISTS, \
    COGNITIVE_SPECIALIST, MOTOR_SKILLS_SPECIALIST


class InfantDevScreening6Months(ChildCrfModelMixin):
    hearing = models.CharField(
        verbose_name='Moves eyes or head in direction of sounds',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

    )

    hearing_response = models.CharField(
        verbose_name='Responds by making sounds when talked to',
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

    eye_movement = models.CharField(
        verbose_name='Eyes move well together (no squint)',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

    )

    familiar_faces = models.CharField(
        verbose_name='Recognizes familiar faces',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

    )

    looks_at_hands = models.CharField(
        verbose_name='Looks at own hands',
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
        verbose_name='Laughs aloud',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

    )

    diff_cries = models.CharField(
        verbose_name=('Uses different cries or sounds to show hunger, tiredness, '
                      'discomfort'),
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

    motor_skills_hands = models.CharField(
        verbose_name='Grasps toy in each hand',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES

    )

    motor_skills_tummy = models.CharField(
        verbose_name='Lifts head when lying on tummy',
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
        verbose_name = 'Infant Developmental Screening for 6 Months'
        verbose_name_plural = 'Infant Developmental Screening for 6 Months'
