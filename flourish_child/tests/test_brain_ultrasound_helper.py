from unittest import mock
from unittest.mock import patch

from django.test import tag, TestCase
from requests.exceptions import RequestException

from flourish_child.helper_classes.brain_ultrasound_helper import BrainUltrasoundHelper


@tag('buh')
class TestBrainUltrasoundHelper(TestCase):

    @mock.patch(
        'flourish_child.helper_classes.brain_ultrasound_helper.site_visit_schedules')
    @mock.patch('flourish_child.helper_classes.brain_ultrasound_helper.django_apps')
    def test_brain_ultrasound_enrolment(self, mock_apps, mock_schedules):
        # Mocking required values
        mock_apps.get_model.return_value = mock.MagicMock()
        mock_schedules.get_by_onschedule_model_schedule_name.return_value = (
            None, mock.MagicMock())
        brain_ultrasound_helper = BrainUltrasoundHelper('child-identifier',
                                                        'caregiver-identifier')
        brain_ultrasound_helper.brain_ultrasound_enrolment()

        # Check if methods are called with expected parameters
        assert mock_apps.get_model.call_count == 2
        assert mock_schedules.get_by_onschedule_model_schedule_name.call_count == 2

    @mock.patch('flourish_child.helper_classes.brain_ultrasound_helper.requests')
    @mock.patch('flourish_child.helper_classes.brain_ultrasound_helper.settings')
    def test_is_enrolled_brain_ultrasound_success(self, mock_settings, mock_requests):
        # Mocking request.post().json() to return True
        mock_requests.post.return_value.json.return_value = True
        brain_ultrasound_helper = BrainUltrasoundHelper('child-identifier',
                                                        'caregiver-identifier')

        self.assertEqual(brain_ultrasound_helper.is_enrolled_brain_ultrasound(), True)

    @mock.patch('flourish_child.helper_classes.brain_ultrasound_helper.logger')
    @patch('requests.post')
    def test_is_enrolled_brain_ultrasound_failure(self, mock_post, mock_logger):
        # Arrange: set up the mock object to simulate RequestException
        mock_post.side_effect = RequestException('Mocked Exception')

        brain_ultrasound_helper = BrainUltrasoundHelper('child-identifier',
                                                        'caregiver-identifier')
        result = brain_ultrasound_helper.is_enrolled_brain_ultrasound()

        self.assertFalse(result)

        mock_logger.error.assert_called_once_with('Error: Mocked Exception')
