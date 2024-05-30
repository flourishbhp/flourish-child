import json
import logging
from datetime import datetime
from flourish_caregiver.helper_classes.maternal_status_helper import MaternalStatusHelper
import requests
from django.apps import apps as django_apps
from django.conf import settings
from edc_base import get_utcnow
from edc_visit_schedule import site_visit_schedules
from edc_constants.constants import POS

from flourish_child.helper_classes.utils import child_utils

logger = logging.getLogger(__name__)


class BrainUltrasoundHelper:

    child_bu_onschedule_model = 'flourish_child.onschedulechildbrainultrasound'
    child_bu_schedule_name = 'child_bu_schedule'

    def __init__(self, child_subject_identifier, caregiver_subject_identifier):
        self.child_subject_identifier = child_subject_identifier
        self.caregiver_subject_identifier = caregiver_subject_identifier

    @property
    def get_child_number(self):
        child_consnet = child_utils.caregiver_child_consent_obj(
            self.child_subject_identifier)
        return child_consnet.caregiver_visit_count if child_consnet else None

    @property
    def brain_ultrasound_schedules(self):

        return [
            {
                'schedule_name': self.child_bu_schedule_name,
                'subject_identifier': self.child_subject_identifier,
                'onschedule_model': self.child_bu_onschedule_model,
            },
            {
                'schedule_name': 'caregiver_bu_schedule_{0}'.format(self.get_child_number),
                'subject_identifier': self.caregiver_subject_identifier,
                'onschedule_model': 'flourish_caregiver.onschedulecaregiverbrainultrasound',
            }
        ]

    @property
    def is_onschedule(self):
        return django_apps.get_model(self.child_bu_onschedule_model).objects.filter(
            subject_identifier=self.child_subject_identifier,
            schedule_name=self.child_bu_schedule_name,
        ).exists()

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model('flourish_caregiver.antenatalenrollment')

    def brain_ultrasound_enrolment(self):
        """Enrols the child into the brain ultrasound schedule.
        """

        for schedule in self.brain_ultrasound_schedules:
            onschedule_model_cls = django_apps.get_model(
                schedule.get('onschedule_model'))
            schedule_name = schedule.get('schedule_name')
            _, new_schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                name=schedule.get('schedule_name'),
                onschedule_model=schedule.get('onschedule_model'))

            if not new_schedule.is_onschedule(
                    subject_identifier=schedule.get('subject_identifier'),
                    report_datetime=get_utcnow()
            ):
                new_schedule.put_on_schedule(
                    subject_identifier=schedule.get('subject_identifier'),
                    schedule_name=schedule.get('schedule_name'))

            if len(schedule.get('subject_identifier').split('-')) == 3:
                try:
                    onschedule_model_cls.objects.get(
                        subject_identifier=schedule.get('subject_identifier'),
                        schedule_name=schedule_name,
                        child_subject_identifier=self.child_subject_identifier)
                except onschedule_model_cls.DoesNotExist:
                    try:
                        onschedule_obj = new_schedule.onschedule_model_cls.objects.get(
                            subject_identifier=schedule.get(
                                'subject_identifier'),
                            schedule_name=schedule_name,
                            child_subject_identifier='')
                    except new_schedule.onschedule_model_cls.DoesNotExist:
                        raise ValueError(Exception('Failed to put subject on '
                                                   f'{schedule_name}'))
                    else:
                        onschedule_obj.child_subject_identifier = (
                            self.child_subject_identifier)
                        onschedule_obj.save()

    def is_enrolled_brain_ultrasound(self):
        """Returns True if the child is enrolled on the brain ultrasound schedule."""

        data = {
            'token': getattr(settings, 'REDCAP_API_TOKEN', None),
            'content': 'record',
            'action': 'export',
            'format': 'json',
            'type': 'flat',
            'csvDelimiter': '',
            'records[0]': self.caregiver_subject_identifier,
            'forms[0]': 'ultrasound_consent_form_version_40',
            'events[0]': 'reconsent_arm_1',
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'exportSurveyFields': 'false',
            'exportDataAccessGroups': 'false',
            'returnFormat': 'json',
        }

        try:
            results = requests.post(
                getattr(settings, 'REDCAP_API_URL', ''), data=data)
            results.raise_for_status()
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error(f'Error: {e}')
        else:
            fields = ['reviewed_v4', 'answered_v4',
                      'asked_v4', 'verified_v4', 'copy_v4']
            try:
                json_result = results.json()
                if json_result and isinstance(json_result[0], dict):
                    return all(json_result[0].get(field) == '1' for field in fields)
            except json.JSONDecodeError:
                logger.error('Invalid JSON response: {}'.format(results.text))
        return False

    def show_brain_ultrasound_button(self):
        antenatal_enrollment_obj = self.antenatal_enrollment_cls.objects.filter(
            child_subject_identifier=self.child_subject_identifier).exists()
        child_age = child_utils.child_age(
            self.child_subject_identifier, datetime.today().date())

        return not self.is_onschedule and antenatal_enrollment_obj and child_age and 0.4 <= child_age <= 0.5
