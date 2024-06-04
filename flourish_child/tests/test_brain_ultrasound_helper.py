from unittest import mock
from unittest.mock import patch

from django.test import tag, TestCase
from edc_base import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from requests.exceptions import RequestException

from flourish_caregiver.models.onschedule import OnScheduleCaregiverBrainUltrasound
from flourish_child.helper_classes.brain_ultrasound_helper import BrainUltrasoundHelper
from flourish_child.models import ChildDummySubjectConsent
from flourish_child.models.onschedule import OnScheduleChildBrainUltrasound


@tag('buh')
class TestBrainUltrasoundHelper(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen', )

        self.options.update(version=3)

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            **self.options)

        self.child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=None,
            first_name=None,
            last_name=None)

        child_consent, _ = ChildDummySubjectConsent.objects.get_or_create(
            subject_identifier=self.child_consent.subject_identifier,
            consent_datetime=get_utcnow(),
        )
        child_consent.save()

    def test_brain_ultrasound_enrolment_edc(self):
        brain_ultrasound_helper = BrainUltrasoundHelper(
            self.child_consent.subject_identifier,
            self.subject_consent.subject_identifier)
        brain_ultrasound_helper.brain_ultrasound_enrolment()

        self.assertEqual(OnScheduleChildBrainUltrasound.objects.filter(
            subject_identifier=self.child_consent.subject_identifier,
            schedule_name='child_bu_schedule').count(), 1)

        self.assertEqual(OnScheduleCaregiverBrainUltrasound.objects.filter(
            subject_identifier=self.subject_consent.subject_identifier,
            schedule_name='caregiver_bu_schedule_1').count(), 1)

    @mock.patch(
        'flourish_child.helper_classes.brain_ultrasound_helper.site_visit_schedules')
    @mock.patch('flourish_child.helper_classes.brain_ultrasound_helper.django_apps')
    def test_brain_ultrasound_enrolment(self, mock_apps, mock_schedules):
        mock_apps.get_model.return_value = mock.MagicMock()
        mock_schedules.get_by_onschedule_model_schedule_name.return_value = (
            None, mock.MagicMock())
        brain_ultrasound_helper = BrainUltrasoundHelper(
            self.child_consent.subject_identifier,
            self.subject_consent.subject_identifier)
        brain_ultrasound_helper.brain_ultrasound_enrolment()

        assert mock_apps.get_model.call_count == 2
        assert mock_schedules.get_by_onschedule_model_schedule_name.call_count == 2

    @mock.patch('flourish_child.helper_classes.brain_ultrasound_helper.requests')
    @mock.patch('flourish_child.helper_classes.brain_ultrasound_helper.settings')
    def test_is_enrolled_brain_ultrasound_success(self, mock_settings, mock_requests):
        mock_requests.post.return_value.json.return_value = [
            {'reviewed_v4': '1', 'answered_v4': '1', 'asked_v4': '1', 'verified_v4': '1',
             'copy_v4': '1'}]
        brain_ultrasound_helper = BrainUltrasoundHelper(
            self.child_consent.subject_identifier,
            self.subject_consent.subject_identifier)

        self.assertTrue(brain_ultrasound_helper.is_enrolled_brain_ultrasound())

    @mock.patch('flourish_child.helper_classes.brain_ultrasound_helper.logger')
    @patch('requests.post')
    def test_is_enrolled_brain_ultrasound_failure(self, mock_post, mock_logger):
        mock_post.side_effect = RequestException('Mocked Exception')

        brain_ultrasound_helper = BrainUltrasoundHelper(
            self.child_consent.subject_identifier,
            self.subject_consent.subject_identifier)
        result = brain_ultrasound_helper.is_enrolled_brain_ultrasound()

        self.assertFalse(result)

        mock_logger.error.assert_called_once_with('Error: Mocked Exception')
