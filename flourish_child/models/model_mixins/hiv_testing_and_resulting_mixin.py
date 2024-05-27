from django.db import models
from edc_appointment.creators import UnscheduledAppointmentCreator
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO
from edc_constants.constants import IND, PENDING, UNKNOWN

from flourish_child.choices import DELIVERY_LOCATION, POS_NEG_PENDING_UNKNOWN


class HIVTestingAndResultingMixin(models.Model):
    child_test_date_estimated = models.CharField(
        verbose_name='Was this date estimated?',
        choices=YES_NO,
        max_length=20,
    )

    test_location = models.CharField(
        verbose_name='Where was the test done?',
        choices=DELIVERY_LOCATION,
        max_length=100,
    )

    test_location_other = OtherCharField()

    results_received = models.CharField(
        verbose_name='Have you received the results of this test?',
        choices=YES_NO,
        max_length=20,
        help_text='request participant to seek HIV Results from clinic'
    )

    recall_result_date = models.CharField(
        verbose_name='Do you recall the date you received this test result, or even the '
                     'month?',
        choices=YES_NO,
        max_length=20,
        null=True,
        blank=True
    )

    received_date = models.DateField(
        verbose_name='What date did you receive this test?',
        null=True,
        blank=True
    )

    result_date_estimated = models.CharField(
        verbose_name='Was this date estimated?',
        choices=YES_NO,
        max_length=20,
        null=True,
        blank=True
    )

    hiv_test_result = models.CharField(
        verbose_name='What is the result of the HIV test?',
        choices=POS_NEG_PENDING_UNKNOWN,
        max_length=20,
        null=True,
        blank=True
    )

    additional_comments = models.TextField(
        verbose_name='Additional comments:',
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        no_results = [IND, PENDING, UNKNOWN]
        if self.hiv_test_result in no_results:
            appointment_creator = UnscheduledAppointmentCreator(
                subject_identifier=self.child_visit.subject_identifier,
                visit_schedule_name=self.child_visit.appointment.visit_schedule_name,
                schedule_name=self.child_visit.appointment.schedule_name,
                visit_code=self.child_visit.appointment.visit_code,
                facility=self.child_visit.appointment.facility,
                timepoint_datetime=self.child_visit.appointment.timepoint_datetime,
            )
            obj = appointment_creator.appointment
            obj.save()

    class Meta:
        abstract = True
