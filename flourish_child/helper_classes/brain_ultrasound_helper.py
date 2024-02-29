import json
import logging

import requests
from django.apps import apps as django_apps
from django.conf import settings
from edc_base import get_utcnow
from edc_visit_schedule import site_visit_schedules

from flourish_child.helper_classes.utils import child_utils

logger = logging.getLogger(__name__)


class BrainUltrasoundHelper:
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
            {'schedule_name': 'caregiver_bu_schedule_{0}'.format(
                self.get_child_number),
                'subject_identifier': self.caregiver_subject_identifier,
                'onschedule_model':
                    'flourish_caregiver.onschedulecaregiverbrainultrasound',
            },
            {'schedule_name': 'child_bu_schedule',
             'subject_identifier': self.child_subject_identifier,
             'onschedule_model': 'flourish_child.onschedulechildbrainultrasound',
             },
        ]

    @property
    def is_onschedule(self):
        return all(
            django_apps.get_model(schedule.get('onschedule_model')).objects.filter(
                subject_identifier=schedule.get('subject_identifier'),
                schedule_name=schedule.get('schedule_name'),
            ).exists()
            for schedule in self.brain_ultrasound_schedules if schedule.get(
                'subject_identifier') == self.child_subject_identifier
        )

    def brain_ultrasound_enrolment(self):
        """Enrols the child into the brain ultrasound schedule.
        """

        for schedule in self.brain_ultrasound_schedules:
            onschedule_model_cls = django_apps.get_model(schedule.get('onschedule_model'))
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
                            subject_identifier=schedule.get('subject_identifier'),
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
            'token': settings.REDCAP_API_TOKEN,
            'content': 'record',
            'action': 'export',
            'format': 'json',
            'type': 'flat',
            'csvDelimiter': '',
            'records[0]': self.caregiver_subject_identifier,
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'exportSurveyFields': 'false',
            'exportDataAccessGroups': 'false',
            'returnFormat': 'json',
            'forms[0]': 'ultrasound_consent_form_version_40',
        }

        try:
            results = requests.post(settings.REDCAP_API_URL, data=data)
            results.raise_for_status()
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error(f'Error: {e}')
        else:
            try:
                json_result = results.json()
                if json_result:
                    return any(isinstance(obj, dict) and any(
                        value != '' for value in obj.values()) for obj in
                               json_result)
            except json.JSONDecodeError:
                logger.error('Invalid JSON response: {}'.format(results.text))
        return False
