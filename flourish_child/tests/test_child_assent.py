import re

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from model_mommy import mommy

from ..models import ChildAssent
from edc_constants.constants import NO, YES


child_identifier = '142\-[0-9\-]+\-10'


class TestChildAssent(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants')

        consent_options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'remain_in_study': YES,
            'hiv_testing': YES,
            'breastfeed_intent': YES,
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES,
            'consent_copy': YES}

        mommy.make_recipe('flourish_caregiver.subjectconsent', **consent_options)

        self.eligible_options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'dob': get_utcnow() - relativedelta(years=8),
            'remain_in_study': YES,
            'hiv_testing': YES,
            'preg_testing': YES}

    def test_allocated_subject_identifier_invalid(self):
        """Test assent does not allocate subject identifier on
        save if participant is ineligible.
        """
        self.eligible_options['remain_in_study'] = NO
        mommy.make_recipe('flourish_child.childassent', **self.eligible_options)
        self.assertIsNone(ChildAssent.objects.all()[0].subject_identifier)

    def test_allocated_subject_identifier(self):
        """Test assent allocates subject identifier on save if participant
        is eligible.
        """
        mommy.make_recipe('flourish_child.childassent', **self.eligible_options)
        self.assertTrue(
            re.match(
                child_identifier,
                ChildAssent.objects.all()[0].subject_identifier))

    def test_assent_creates_registered_subject_invalid(self):
        """Test assent does not create a registered subject on
            save if participant is ineligible.
        """
        self.eligible_options['remain_in_study'] = NO
        self.assertEquals(RegisteredSubject.objects.all().count(), 1)
        mommy.make_recipe('flourish_child.childassent', **self.eligible_options)
        self.assertEquals(RegisteredSubject.objects.all().count(), 1)

    def test_assent_creates_registered_subject(self):
        """Test consent creates a registered subject on save if participant is eligible.
        """
        self.assertEquals(RegisteredSubject.objects.all().count(), 1)
        mommy.make_recipe('flourish_child.childassent', **self.eligible_options)
        self.assertEquals(RegisteredSubject.objects.all().count(), 2)
