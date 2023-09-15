from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base import get_utcnow
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start

from flourish_child.choices import BORN, CHILD_TYPE, DELIVERY_LOCATION, \
    DELIVERY_METHOD, GESTATIONAL_AGE_KNOWN


class PreFlourishBirthData(SiteModelMixin, NonUniqueSubjectIdentifierFieldMixin,
                           BaseUuidModel):
    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use'
                   ' the date/time this information was reported.'))

    dob = models.DateField(
        verbose_name="Child's date of birth")

    place_of_birth = models.CharField(
        verbose_name='Location of delivery',
        choices=DELIVERY_LOCATION,
        max_length=50)

    other_place_of_birth = OtherCharField()

    method_of_delivery = models.CharField(
        verbose_name='Method of delivery',
        choices=DELIVERY_METHOD,
        max_length=10)

    gestational_age_known = models.CharField(
        verbose_name='Is the gestational age known for this child',
        choices=GESTATIONAL_AGE_KNOWN,
        max_length=20)

    gestational_age_weeks = models.IntegerField(
        verbose_name='What was the gestation age in weeks',
        validators=[MinValueValidator(20), MaxValueValidator(43), ],
        blank=True,
        null=True)

    gestational_age_months = models.IntegerField(
        verbose_name='What was the gestation age in months',
        validators=[MinValueValidator(5), MaxValueValidator(9), ],
        blank=True,
        null=True)

    was_child_born = models.CharField(
        verbose_name='Was this child born',
        choices=BORN,
        max_length=15)

    child_type = models.CharField(
        verbose_name='Was this child one of the following',
        choices=CHILD_TYPE,
        max_length=15)

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Pre Flourish Birth Data'
        verbose_name_plural = 'Pre Flourish Birth Data'
