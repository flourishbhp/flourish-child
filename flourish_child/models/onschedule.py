from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager
from edc_visit_schedule.model_mixins import OnScheduleModelMixin as BaseOnScheduleModelMixin


class OnScheduleModelMixin(BaseOnScheduleModelMixin, BaseUuidModel):
    """A model used by the system. Auto-completed by enrollment model.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    schedule_name = models.CharField(max_length=25,
                                     blank=True,
                                     null=True)

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    def put_on_schedule(self):
        pass

    def save(self, *args, **kwargs):
        self.consent_version = '1'
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
        abstract = True


class OnScheduleChildCohortAEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortABirth(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortAQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCPool(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortASec(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortBSec(OnScheduleModelMixin):
    pass


class OnScheduleChildCohortCSec(OnScheduleModelMixin):
    pass

