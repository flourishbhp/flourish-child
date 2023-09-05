from django.apps import apps as django_apps
from datetime import date
from dateutil.relativedelta import relativedelta
from edc_base.utils import age


class ChildFollowUpBookingHelper(object):
    """Class that creates a follow up booking for participant on the calendar
    """

    def __init__(self, subject_identifier=None, ):
        self.subject_identifier = subject_identifier
        self.participant_note_cls = django_apps.get_model('flourish_calendar.participantnote')

    def schedule_fu_booking(self, subject_identifier, booking_dt=None):
        """ Schedule participant for follow up booking, a year after their enrollment,
            considerations made for priority of booking based off `child_age` per `cohort`
            if child near aging out. Reschedule less priority participant to next available
            slot on the calendar.
            @param subject_identifier: Participant identifier
            @param booking_dt: Date to schedule participant against
        """
        # Check participant is not already scheduled for FU
        if self.is_scheduled(subject_identifier):
            return
        cutoff_date = date(2025, 4, 30)

        while booking_dt.date() < cutoff_date:
            # Check booking date does not fall on holiday or weekend before scheduling.
            # If falls on weekend push date to next day.
            is_holiday_or_weekend = self.check_date(booking_dt)
            if is_holiday_or_weekend:
                booking_dt = booking_dt + relativedelta(days=1)
                continue

            slots_available, scheduled_sidx = self.check_availability(booking_dt, max_possible=3)
            if slots_available:
                self.create_booking(subject_identifier, booking_dt)
                break
            else:
                priorities = self.assign_priority(subject_identifier, scheduled_sidx, booking_dt)
                if not priorities.get(subject_identifier):
                    subject_identifier = subject_identifier
                elif all(priorities.values()):
                    # Alert clinic team system tried to schedule `pid` on `date` but
                    # failed due to multiple priorities.
                    break
                else:
                    low_priorities = [idx for idx in priorities.keys() if not priorities.get(idx)]
                    reschedule = low_priorities[0]
                    for idx in low_priorities[1:]:
                        child1_dob = self.get_child_data(reschedule).child_dob
                        child2_dob = self.get_child_data(idx).child_dob
                        if child2_dob > child1_dob:
                            reschedule = idx
                    # Remove participant with lower priority from booking date.
                    self.remove_booking(reschedule, booking_dt)
                    # Add the high priority participant against date.
                    self.create_booking(subject_identifier, booking_dt)
                    # Assign the subject_identifier to participant to be rescheduled
                    # for the next day of week.
                    subject_identifier = reschedule
                # Update booking date, to next day of week
                booking_dt = booking_dt + relativedelta(days=1)

    def check_date(self, booking_date):
        """ Check if booking date falls within a holiday or weekend
            @param booking_date: Date to schedule
            @return: True if holiday or weekend else False
        """
        facility_app_config = django_apps.get_app_config('edc_facility')

        facility = facility_app_config.get_facility('5-day clinic')

        is_holiday = facility.holidays.holidays.filter(local_date=booking_date.date())
        is_weekend = booking_date.weekday() >= 5

        return is_holiday or is_weekend

    def check_availability(self, booking_date, max_possible):
        """ Confirm date to be booked does not have the max possible participant booked
            against the date already.
            @param booking_date: Date to schedule
            @param max_possible: Maximum number of participant's booked per day.
            @return: True if slots available else False, and list of scheduled participants on a date. 
        """
        fu_notes = self.participant_note_cls.objects.filter(
            title='Follow Up Schedule', date=booking_date.date()).values_list('subject_identifier', flat=True)
        return max_possible > fu_notes.count(), fu_notes

    def is_scheduled(self, subject_identifier):
        return self.participant_note_cls.objects.filter(
            subject_identifier=subject_identifier,
            title='Follow Up Schedule').exists()
            

    def create_booking(self, subject_identifier, booking_date):
        self.participant_note_cls.objects.create(
            subject_identifier=subject_identifier,
            title='Follow Up Schedule',
            date=booking_date.date())

    def remove_booking(self, subject_identifier, booking_date):
        try:
            booking = self.participant_note_cls.objects.get(
                subject_identifier=subject_identifier,
                date=booking_date.date(),
                title='Follow Up Schedule')
        except self.participant_note_cls.DoesNotExist:
            pass
        else:
            booking.delete()

    def assign_priority(self, subject_identifier, scheduled_sidx, booking_dt):
        priorities = {}
        scheduled_sidx = list(scheduled_sidx)
        scheduled_sidx.append(subject_identifier)
        for child_sid in scheduled_sidx:
            priorities.update({f'{child_sid}': False})
            child_consent = self.get_child_data(child_sid)
            child_age = self.age_in_years(age(child_consent.child_dob, booking_dt.date()))
            cohort = child_consent.cohort
            if child_consent.preg_enroll:
                child_anc_limit = booking_dt - relativedelta(months=18)
                child_anc_lower = child_anc_limit - relativedelta(days=45)
                child_anc_upper = child_anc_limit + relativedelta(days=45)

                anc_lower_age = self.age_in_years(age(child_anc_lower, booking_dt))
                anc_upper_age = self.age_in_years(age(child_anc_upper, booking_dt))
                if anc_lower_age < child_age and anc_upper_age > anc_upper_age:
                    priorities.update({f'{child_sid}': True})
                    continue
                continue
            elif cohort == 'cohort_a' and ((4 + 5/12) <= child_age and 5 >= child_age):
                priorities.update({f'{child_sid}': True})
                continue
            elif cohort == 'cohort_b' and (5 <= child_age and (10 + 5/12) > child_age):
                priorities.update({f'{child_sid}': True})
        return priorities

    def get_child_data(self, subject_identifier):
        child_consent_cls = django_apps.get_model('flourish_caregiver.caregiverchildconsent')
        consents = child_consent_cls.objects.filter(
            subject_identifier=subject_identifier).only(
                'subject_identifier', 'cohort', 'child_dob')
        return consents[0]

    def age_in_years(self, age_rdelta):
        return (age_rdelta.years + age_rdelta.months/12)
