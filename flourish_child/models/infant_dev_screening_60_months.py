from django.db import models
from edc_constants.constants import YES

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import YES_NO_DONT_KNOW, HEARING_SPECIALISTS, VISION_SPECIALISTS, \
    COGNITIVE_SPECIALIST, MOTOR_SKILLS_SPECIALIST


class InfantDevScreening60Months(ChildCrfModelMixin):
    speak = models.CharField(
        verbose_name='Speaks in full sentences',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    hearing_response = models.CharField(
        verbose_name='Caregiver understands child’s speech',
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

    vision_problems = models.CharField(
        verbose_name='No reported/observed vision problems (use illiterate E chart if available)',
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

    interactive = models.CharField(
        verbose_name='Interacts with children and adults',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    understand_commands = models.CharField(
        verbose_name='Understands multiple commands',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES,
        help_text='e.g., go to the kitchen and bring me your plate'

    )

    cognitive_specialist = models.CharField(
        verbose_name=('Referred to any of the following specialists for'
                      ' Cognitive/Behavior'),
        choices=COGNITIVE_SPECIALIST,
        max_length=30,
        default=''
    )

    motor_skills_hops = models.CharField(
        verbose_name='Hops on one foot',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    motor_skills_drawing = models.CharField(
        verbose_name='Holds with fingers at top or middle of pencil or stick to draw',
        choices=YES_NO_DONT_KNOW,
        max_length=15,
        default=YES
    )

    motor_skills_dress = models.CharField(
        verbose_name='Dresses self',
        choices=YES_NO_DONT_KNOW,
        max_length=30,
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
        verbose_name = 'Infant Developmental Screening for Age 60 Months '
        verbose_name_plural = 'Infant Developmental Screening for Age 60 Months'
