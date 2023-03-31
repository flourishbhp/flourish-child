from django.db import models
from edc_constants.constants import YES

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import YES_NO_DONT_KNOW, HEARING_SPECIALISTS, VISION_SPECIALISTS, \
    COGNITIVE_SPECIALIST, MOTOR_SKILLS_SPECIALIST


class InfantDevScreening36Months(ChildCrfModelMixin):
    speaking = models.CharField(
        verbose_name='Child speaks in simple 3 word sentences ',
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

    vision = models.CharField(
        verbose_name='Sees small shapes clearly at a distance (across room)',
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

    play_with_people = models.CharField(
        verbose_name='Plays with other children/adults',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    play_with_toys = models.CharField(
        verbose_name='Uses pretend play (e.g., feeds doll) ',
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

    runs_well = models.CharField(
        verbose_name='Runs well',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    self_feed = models.CharField(
        verbose_name='Eats on own ',
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
        verbose_name = 'Infant Developmental Screening for 3 years/36 Months '
        verbose_name_plural = 'Infant Developmental Screening for 3 years/36 Months'
