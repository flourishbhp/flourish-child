from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import tag, TestCase
from edc_appointment.models import Appointment as CaregiverAppointment
from edc_base.utils import get_utcnow
from edc_constants.constants import NEG, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import RequisitionMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..models import Appointment, ChildDummySubjectConsent, OnScheduleChildCohortABirth

app_config = django_apps.get_app_config('flourish_child')


@tag('dev_screening')
class TestBirthRequisitions(TestCase):
    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': app_config.consent_version
        }

        self.screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',
        )

        self.preg_subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

    @tag('ipcp')
    def test_infant_pl_cytokines_panel_required(self):
        """Test that the infant pl cytokines panel is required"""
        preg_caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.preg_subject_consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None,
            version='2.1')

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        caregiver_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=CaregiverAppointment.objects.get(
                subject_identifier=self.preg_subject_consent.subject_identifier,
                visit_code='1000M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.ultrasound',
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            maternal_visit=caregiver_visit, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            delivery_datetime=get_utcnow(),
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),
            user_created='imosweu')
        child_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
        )

        child_consent.dob = (get_utcnow() - relativedelta(days=1)).date()
        child_consent.save_base(raw=True)
        """Test that the infant pl cytokines panel is required"""
        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            visit_code_sequence=0,
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortABirth.objects.filter(
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            schedule_name='child_a_birth_schedule1').count(), 1)

        self.assertEqual(RequisitionMetadata.objects.get(
            model='flourish_child.childrequisition',
            panel_name='infant_pl_cytokines',
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2000D').entry_status, REQUIRED)

    @tag('ipcp')
    def test_infant_pl_cytokines_panel_not_required(self):
        """Test that the infant pl cytokines panel is not required"""

        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

        consent_version_obj = consent_version_cls.objects.get(
            screening_identifier=self.preg_subject_consent.screening_identifier)

        consent_version_obj.child_version = '2'
        consent_version_obj.save()

        preg_caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.preg_subject_consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None, )

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        caregiver_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=CaregiverAppointment.objects.get(
                subject_identifier=self.preg_subject_consent.subject_identifier,
                visit_code='1000M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.ultrasound',
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            maternal_visit=caregiver_visit, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            child_subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            delivery_datetime=get_utcnow(),
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),
            user_created='imosweu')
        child_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
        )

        child_consent.dob = (get_utcnow() - relativedelta(days=1)).date()
        child_consent.save_base(raw=True)
        """Test that the infant pl cytokines panel is required"""
        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            visit_code_sequence=0,
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortABirth.objects.filter(
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            schedule_name='child_a_birth_schedule1').count(), 1)

        self.assertEqual(RequisitionMetadata.objects.get(
            model='flourish_child.childrequisition',
            panel_name='infant_pl_cytokines',
            subject_identifier=preg_caregiver_child_consent_obj.subject_identifier,
            visit_code='2000D').entry_status, NOT_REQUIRED)
