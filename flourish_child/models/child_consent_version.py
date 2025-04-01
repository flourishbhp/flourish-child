from django.apps import apps as django_apps
from django.db import models
from django.utils import timezone
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future, datetime_is_future
from edc_base.sites import SiteModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugModelMixin

from ..choices import CONSENT_VERSION

child_config = django_apps.get_app_config('flourish_child')


class ChildConsentVersion(SiteModelMixin, SearchSlugModelMixin,
                          BaseUuidModel):

    subject_identifier = models.CharField(
        verbose_name='Subject Identifier',
        max_length=50,
        unique=True)

    version = models.CharField(
        verbose_name=('Which version of the child consent would you '
                      'like to be consented with?'),
        choices=CONSENT_VERSION,
        max_length=3)

    report_datetime = models.DateTimeField(
        verbose_name='Report datetime.',
        default=timezone.now,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
            datetime_is_future
        ])

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Child Consent Version'
        verbose_name_plural = 'Child Consent Version'
