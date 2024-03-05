from dateutil.relativedelta import relativedelta
from django.test import tag, TestCase
from django.utils.datetime_safe import datetime
from edc_base.utils import get_utcnow
from edc_constants.constants import NEG, NO, POS, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata, RequisitionMetadata
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..models import Appointment, ChildDummySubjectConsent, \
    OnScheduleChildCohortAQuarterly


@tag('testrg')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '2'
        }

        self.screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',
        )

        self.preg_subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.screening_preg.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        self.preg_caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.preg_subject_consent,
            gender=None,
            first_name=None,
            last_name=None,
            identity=None,
            confirm_identity=None,
            study_child_identifier=None,
            child_dob=None,
            version='2')

        self.preg_subject_identifier = self.preg_subject_consent.subject_identifier

    @tag('bexm')
    def test_birthexam_required(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            delivery_datetime=get_utcnow(),
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),
            user_created='imosweu')

        child_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
        )

        child_consent.dob = (get_utcnow() - relativedelta(days=1)).date()
        child_consent.save_base(raw=True)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            is_present=YES,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.birthexam',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D').entry_status, REQUIRED)

    @tag('bexm')
    def test_birthexam_not_required(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            delivery_datetime=get_utcnow(),
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),
            user_created='imosweu')

        child_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
        )

        child_consent.dob = (get_utcnow() - relativedelta(days=1)).date()
        child_consent.save_base(raw=True)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            is_present=NO,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.birthexam',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D').entry_status, NOT_REQUIRED)

    @tag('bdt')
    def test_birthdata_required(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            delivery_datetime=get_utcnow(),
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(),
            user_created='imosweu')

        child_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
        )

        child_consent.dob = (get_utcnow() - relativedelta(days=1)).date()
        child_consent.save_base(raw=True)

        visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.birthdata',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D').entry_status, REQUIRED)

        mommy.make_recipe(
            'flourish_child.birthdata',
            child_visit=visit,
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.birthdata',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001').entry_status, NOT_REQUIRED)

    @tag('fsc1')
    def test_foodsecquestionnaire_required(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            live_infants_to_register=1)

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(months=36)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(OnScheduleChildCohortAQuarterly.objects.filter(
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            schedule_name='child_a_quart_schedule1').count(), 1)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childfoodsecurityquestionnaire',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001').entry_status, NOT_REQUIRED)

    def test_arv_exposure_required_if_pos(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvexposure',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D',
                visit_code_sequence='0').entry_status, REQUIRED)

    def test_arv_exposure_not_required_if_neg(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvexposure',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_dna_pcr_not_required_if_birth(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            RequisitionMetadata.objects.get(
                model='flourish_child.childrequisition',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D',
                panel_name='dna_pcr',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_infant_hiv_test_preg_valid(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infanthivtesting',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001', ).entry_status, REQUIRED)

    def test_infant_hiv_test_infant_feeding_required(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2003'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_visit_4 = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2004'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.infantfeeding',
            child_visit=child_visit_4,
            continuing_to_bf=YES,
        )

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infanthivtesting',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2004', ).entry_status, REQUIRED)

    @tag('tihtifht')
    def test_infant_hiv_test_infant_feeding_hiv_test(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            enrollment_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.infantfeeding',
            child_visit=child_visit,
            continuing_to_bf=NO,
            dt_weaned=datetime(2023, 5, 24)
        )

        mommy.make_recipe(
            'flourish_child.infanthivtesting',
            child_visit=child_visit,
            received_date=datetime(2023, 6, 5),
            child_tested_for_hiv=NO,
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infanthivtesting',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002', ).entry_status, REQUIRED)

    def test_infant_hiv_test_infant_feeding_not_required(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.infantfeeding',
            child_visit=child_visit,
            continuing_to_bf=NO,
            dt_weaned=datetime(2023, 6, 2)
        )

        mommy.make_recipe(
            'flourish_child.infanthivtesting',
            child_visit=child_visit,
            received_date=datetime(2023, 8, 5)
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2003'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infanthivtesting',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2003', ).entry_status, NOT_REQUIRED)

    def test_skip_infant_hiv_test_q2_if_tested_q1(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.infanthivtesting',
            child_visit=child_visit,
            child_tested_for_hiv=YES,
            received_date=datetime(2023, 6, 5)
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infanthivtesting',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002', ).entry_status, NOT_REQUIRED)

    def test_require_infant_hiv_test_q2_if_not_tested_q1(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.infanthivtesting',
            child_visit=child_visit,
            child_tested_for_hiv=NO,
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infanthivtesting',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002', ).entry_status, REQUIRED)

    def test_arv_proph_not_required_2000d(self):
        """ Assert ARV prophylaxis crf not required at child birth visit
        """
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.filter(
                model='flourish_child.infantarvprophylaxis',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D', ).exists(), False)

    def test_arv_proph_2001_preg_pos_required(self):
        """ Assert ARV proph crf is required at 2001 if participant is
            ANC enrolled and POS.
        """
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvprophylaxis',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001', ).entry_status, REQUIRED)

    def test_arv_proph_if_missed_at_2001(self):
        """ Assert ARV proph crf is required at next visit if missed at 2001
        """
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvprophylaxis',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002', ).entry_status, REQUIRED)

    def test_arv_proph_if_completed_at_2001(self):
        """ Assert ARV proph crf is not required at next visit(s) if completed at 2001
            and status is not in-progress.
        """
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.infantarvprophylaxis',
            child_visit=child_visit,
            art_status='completed_in_time',
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvprophylaxis',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002', ).entry_status, NOT_REQUIRED)

    def test_arv_proph_status_in_progress(self):
        """ Assert ARV proph crf is required at next visit(s) if status is in-progress.
        """
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.infantarvprophylaxis',
            child_visit=child_visit,
            art_status='in_progress',
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvprophylaxis',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002', ).entry_status, REQUIRED)

    def test_arv_proph_status_in_progress_2003(self):
        """ Assert ARV proph crf is required at next visit(s) if status is in-progress.
        """
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=POS,
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            child_subject_identifier=self.preg_caregiver_child_consent_obj
            .subject_identifier,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_child.childbirth',
            subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(days=1)).date(), )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2000D'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2001'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2002'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.infantarvprophylaxis',
            child_visit=child_visit,
            art_status='in_progress',
        )

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2003'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.infantarvprophylaxis',
                subject_identifier=self.preg_caregiver_child_consent_obj
                .subject_identifier,
                visit_code='2003', ).entry_status, REQUIRED)
