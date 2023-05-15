import pytz
from django.db import models
from django.db.models.deletion import ProtectedError
from edc_appointment.constants import NEW_APPT
from edc_appointment.managers import AppointmentManager as EdcAppointmentManager


class AppointmentManager(EdcAppointmentManager, models.Manager):
    """ Overrides the base appointment manager to remove future appointments
        taking into consideration the window period for new remaining appts.
    """

    def delete_for_subject_after_date(self, subject_identifier, dt, op=None,
                                      visit_schedule_name=None,
                                      schedule_name=None):
        """ Deletes appointments for a given subject_identifier with
            appt datetime covering the window period greater than or equal to
            the `dt`.

        If a visit form exists for any appointment, a ProtectedError will
        be raised.
        """
        valid_ops = ['gt', 'gte']
        op = 'gte' if op is None else op
        if op not in valid_ops:
            raise TypeError('Allowed lookup operators are {}. Got {}.'.format(
                ', '.join(valid_ops), op))
        options = {'subject_identifier': subject_identifier, }
        if schedule_name and not visit_schedule_name:
            raise TypeError(
                f'Expected visit_schedule_name for schedule_name '
                f'\'{schedule_name}\'. Got {visit_schedule_name}')
        if visit_schedule_name:
            try:
                visit_schedule_name, schedule_name = visit_schedule_name.split(
                    '.')
            except ValueError:
                if schedule_name:
                    options.update(dict(schedule_name=schedule_name))
            options.update(dict(visit_schedule_name=visit_schedule_name))

        appt_options = options.copy()
        appt_options.update({f'appt_datetime__{op}': dt})
        future_appts = self.filter(**appt_options).order_by('-timepoint')
        deleted = self.delete_appointment(appointments=future_appts)

        # Checks if there's any new appointments remaining that have a future
        # upper window period opening, and removes them too.
        appt_options = options.copy()
        appt_options.update({f'appt_status': NEW_APPT})
        appointments = self.filter(**appt_options).order_by('-timepoint')
        future_by_upper = []
        for appt in appointments:
            visit_definition = appt.visits.get(appt.visit_code)
            latest_appt_date = (
                appt.timepoint_datetime + visit_definition.rupper).astimezone(
                    pytz.timezone('Africa/Gaborone'))
            if latest_appt_date >= dt:
                future_by_upper.append(appt)
        deleted += self.delete_appointment(appointments=future_by_upper, deleted=deleted)
        return deleted

    def delete_appointment(self, appointments=[], deleted=0):
        for appointment in appointments:
            try:
                appointment.delete()
                deleted += 1
            except ProtectedError:
                break
        return deleted
