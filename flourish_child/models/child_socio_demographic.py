from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from .child_crf_model_mixin import ChildCrfModelMixin
from .model_mixins.child_socio_demographic_mixin import ChildSocioDemographicMixin
from ..choices import CARETAKERS, BUILT_DATES, YES_NO_DONT_KNOW


class ChildSocioDemographic(ChildSocioDemographicMixin, ChildCrfModelMixin):
    """ A model completed by the user on Demographics form for all infants.
    """

    primary_caretaker = models.CharField(
        verbose_name=('Which of the following people would be considered the child\'s '
                      'primary caretaker:'),
        max_length=50,
        choices=CARETAKERS,
        default=''
    )

    primary_caretaker_other = OtherCharField()

    secondary_caretaker = models.CharField(
        verbose_name=('Who provides the second most caretaking responsibilities of the '
                      'child enrolled in FLOURISH:'),
        max_length=50,
        choices=CARETAKERS,
        null=True,
        blank=True
    )

    secondary_caretaker_other = OtherCharField()

    house_painted = models.CharField(
        verbose_name='Is the house the child lives in currently painted on the outside '
                     'or inside?',
        max_length=7,
        choices=YES_NO,
        default=''
    )

    paint_peeling = models.CharField(
        verbose_name='Is there any peeling, shipping or cracking paint in your home?',
        max_length=15,
        choices=YES_NO_DONT_KNOW,
        blank=True,
        null=True,
    )

    building_date = models.CharField(
        verbose_name='When was the house you live in now built?',
        max_length=25,
        choices=BUILT_DATES,
        default=''
    )

    near_busy_road = models.CharField(
        verbose_name='Does the child currently live close to a busy road?',
        choices=YES_NO,
        max_length=7,
        default=''
    )

    busy_road_before = models.CharField(
        verbose_name='Since this child was born, have you ever lived next to a busy '
                     'road?',
        max_length=7,
        choices=YES_NO,
        default=''
    )

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Child Sociodemographic Data Version 2"
        verbose_name_plural = "Child Sociodemographic Data Version 2"
