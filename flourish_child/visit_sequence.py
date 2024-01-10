from django.db import transaction
from edc_visit_tracking.visit_sequence import VisitSequence
from .helper_classes.utils import child_utils


class VisitSequence(VisitSequence):
    """ Override property for previous_visit for sequential enrollment
        or participant's replacing others, appointments continuing off
        where the previous onschedule appts were last done.
    """

    def __init__(self, appointment=None):
        self.appointment = appointment
        self.appointment_model_cls = self.appointment.__class__
        self.model_cls = getattr(
            self.appointment_model_cls,
            self.appointment_model_cls.related_visit_model_attr()
        ).related.related_model
        self.subject_identifier = self.appointment.subject_identifier
        self.visit_schedule_name = self.appointment.visit_schedule_name
        self.visit_code = self.appointment.visit_code
        previous_visit = self.appointment.schedule.visits.previous(
            self.visit_code)
        self.previous_appointment = child_utils.get_previous_appt_instance(self.appointment)
        try:
            self.previous_visit_code = getattr(
                self.previous_appointment, 'visit_code', None) or previous_visit.code
        except AttributeError:
            self.previous_visit_code = None
        self.previous_visit_missing = self.previous_visit_code and not self.previous_visit

    @property
    def previous_visit(self):
        """Returns the previous visit model instance if it exists.
        """
        previous_visit = None
        if self.previous_visit_code:
            with transaction.atomic():
                try:
                    previous_visit = self.model_cls.objects.get(
                        appointment__subject_identifier=self.subject_identifier,
                        visit_schedule_name=self.visit_schedule_name,
                        schedule_name=self.appointment.schedule_name,
                        visit_code=self.previous_visit_code)
                except self.model_cls.DoesNotExist:
                    previous_appointment = self.appointment_model_cls.objects.filter(
                        subject_identifier=self.subject_identifier,
                        visit_code=self.previous_visit_code).order_by(
                            '-visit_code_sequence').first()
                    if previous_appointment:
                        try:
                            previous_visit = self.model_cls.objects.get(
                                appointment=previous_appointment)
                        except self.model_cls.DoesNotExist:
                            pass
                    else:
                        previous_visit = getattr(
                            self.previous_appointment, self.model_cls._meta.model_name, None)
        return previous_visit
