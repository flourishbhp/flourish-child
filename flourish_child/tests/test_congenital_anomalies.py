from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import tag, TestCase
from edc_appointment.models import Appointment as CaregiverAppointment
from edc_base import get_utcnow
from edc_constants.constants import NO, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_child.models import Appointment, ChildVisit

app_config = django_apps.get_app_config('flourish_child')


@tag('congenital_anomalies')
class TestCongenitalAnomalies(TestCase):

    def setUp(self):
        import_holidays()
        self.options = {
            'consent_datetime': get_utcnow(),
            'version': app_config.consent_version}

        screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen', )

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        self.caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=None,
            first_name=None,
            last_name=None,
            version=app_config.consent_version)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            child_subject_identifier=self.caregiver_child_consent_obj.subject_identifier,
            subject_identifier=subject_consent.subject_identifier, )

        caregiver_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=CaregiverAppointment.objects.get(
                subject_identifier=subject_consent.subject_identifier,
                visit_code='1000M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.ultrasound',
            child_subject_identifier=self.caregiver_child_consent_obj.subject_identifier,
            maternal_visit=caregiver_visit, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.caregiver_child_consent_obj.subject_identifier,
            subject_identifier=subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.caregiver_child_consent_obj.subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_congenital_anomalies_not_required(self):
        visit = ChildVisit.objects.get(visit_code='2000D')

        mommy.make_recipe('flourish_child.birthdata',
                          congenital_anomalities=NO,
                          child_visit=visit, )
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantcongenitalanomalies',
                subject_identifier=self.caregiver_child_consent_obj.subject_identifier,
                visit_code='2000D').entry_status, NOT_REQUIRED)

    def test_congenital_anomalies_required(self):
        visit = ChildVisit.objects.get(visit_code='2000D')

        mommy.make_recipe('flourish_child.birthdata',
                          congenital_anomalities=YES,
                          child_visit=visit, )
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantcongenitalanomalies',
                subject_identifier=self.caregiver_child_consent_obj.subject_identifier,
                visit_code='2000D').entry_status, REQUIRED)
