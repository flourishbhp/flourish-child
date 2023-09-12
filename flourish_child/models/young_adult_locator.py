from django.apps import apps as django_apps
from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django_crypto_fields.fields import EncryptedCharField
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_action_item.model_mixins import ActionModelMixin
from edc_action_item.action import ActionItemGetter
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber, TelephoneNumber
from edc_base.model_validators.date import date_not_future, datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_DOESNT_WORK
from edc_locator.model_mixins.subject_contact_fields_mixin import SubjectContactFieldsMixin
from edc_locator.model_mixins.subject_indirect_contact_fields_mixin import SubjectIndirectContactFieldsMixin
from edc_locator.model_mixins.subject_work_fields_mixin import SubjectWorkFieldsMixin
from edc_locator.model_mixins.locator_methods_model_mixin import LocatorMethodsModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager
from ..action_items import YOUNG_ADULT_LOCATOR_ACTION
from .model_mixins import SearchSlugModelMixin


class YoungAdultLocatorManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class YoungAdultLocator(SiteModelMixin, SubjectContactFieldsMixin,
                   SubjectIndirectContactFieldsMixin, ActionModelMixin,
                   SubjectWorkFieldsMixin, LocatorMethodsModelMixin,
                   SearchSlugModelMixin, BaseUuidModel):
    action_name = YOUNG_ADULT_LOCATOR_ACTION

    tracking_identifier_prefix = 'CL'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    along_side_caregiver = models.CharField(
        verbose_name='Do you feel comfortable with continuing on the FLOURISH study alongside your caregiver?',
        max_length=3,
        choices=YES_NO,
    )

    locator_date = models.DateField(blank=True, null=True)

    first_name = FirstnameField(
        blank=False,
        null=False,
        verbose_name='First name',)

    last_name = LastnameField(
        blank=False,
        null=False,
        verbose_name='Last name')

    locator_date = models.DateField(
        verbose_name='Date Locator Form signed',
        validators=[date_not_future],)

    may_call = models.CharField(
        max_length=25,
        choices=YES_NO,
        blank=True,
        null=True,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study '
            'staff to call her for follow-up purposes during the study?'))

    may_visit_home = models.CharField(
        max_length=25,
        choices=YES_NO,
        blank=True,
        null=True,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study staff <b>to '
            'make home visits</b> for follow-up purposes during the study?'))

    may_call_work = models.CharField(
        max_length=25,
        choices=YES_NO_DOESNT_WORK,
        blank=True,
        null=True,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study staff '
            'to contact her at work for follow up purposes during the study?'))

    subject_work_phone = EncryptedCharField(
        verbose_name='Work contact number',
        blank=True,
        null=True)

    subject_cell = EncryptedCharField(
        verbose_name="Cell number",
        max_length=8,
        validators=[CellNumber, ],
        blank=True,
        null=True
    )

    may_contact_indirectly = models.CharField(
        max_length=25,
        choices=YES_NO,
        blank=True,
        null=True,
        verbose_name=mark_safe(
            'Has the participant given permission for study staff '
            '<b>to contact anyone else</b> for follow-up purposes during the study?'),
        help_text='For example a partner, spouse, family member, neighbour ...')

    history = HistoricalRecords()

    objects = YoungAdultLocatorManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Young Adults Locator'
