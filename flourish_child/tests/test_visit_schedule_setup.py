from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models import OnScheduleChildCohortA, OnScheduleChildCohortB, OnScheduleChildCohortC


class TestVisitScheduleSetup(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        mommy.make_recipe(
            'flourish_child.registeredsubject',
            subject_identifier='12345678-10',)

    def test_cohort_a_onschedule_consent_valid(self):
        subject_consent = mommy.make_recipe(
            'flourish_child.childdummysubjectconsent',
            subject_identifier='12345678-10',
            **self.options)

        subject_consent.cohort = 'cohort_a'
        subject_consent.save()

        self.assertEqual(OnScheduleChildCohortA.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleChildCohortA.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name,
            'cohort_a_schedule_1')

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 3)

    def test_cohort_b_onschedule_valid(self):
        subject_consent = mommy.make_recipe(
            'flourish_child.childdummysubjectconsent',
            subject_identifier='12345678-10',
            **self.options)

        subject_consent.cohort = 'cohort_b'
        subject_consent.save()

        self.assertEqual(OnScheduleChildCohortB.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleChildCohortB.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name,
            'cohort_b_schedule_1')

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 3)

    def test_cohort_c_onschedule_valid(self):
        subject_consent = mommy.make_recipe(
            'flourish_child.childdummysubjectconsent',
            subject_identifier='12345678-10',
            ** self.options)

        subject_consent.cohort = 'cohort_c'
        subject_consent.save()

        self.assertEqual(OnScheduleChildCohortC.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 1)

        self.assertEqual(OnScheduleChildCohortC.objects.get(
            subject_identifier=subject_consent.subject_identifier).schedule_name,
            'cohort_c_schedule_1')

        self.assertEqual(Appointment.objects.filter(
            subject_identifier=subject_consent.subject_identifier).count(), 3)
