from django.db import models
from django.contrib.sites.models import Site

from edc_appointment.managers import AppointmentManager
from edc_appointment.model_mixins import AppointmentModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_protocol.validators import datetime_not_before_study_start


class Appointment(AppointmentModelMixin, SiteModelMixin, BaseUuidModel):

    appt_datetime = models.DateTimeField(
        verbose_name=('Appointment date and time'),
        validators=[datetime_not_before_study_start],
        db_index=True)

    site = models.ForeignKey(
        Site, on_delete=models.PROTECT, null=True, editable=False,
        related_name='appoimtment_site')

    on_site = CurrentSiteManager()

    objects = AppointmentManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier,
                self.visit_schedule_name,
                self.schedule_name,
                self.visit_code,
                self.visit_code_sequence)

    natural_key.dependencies = ['sites.Site']

    class Meta(AppointmentModelMixin.Meta):
        pass
