from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, YES
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy
from ..helper_classes.child_fu_onschedule_helper import ChildFollowUpEnrolmentHelper
from ..models import Appointment
from edc_metadata.models import CrfMetadata
from edc_metadata.constants import REQUIRED, NOT_REQUIRED


@tag('caid')
class TestCageAidRuleGroup(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=0),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '12345',
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1234'}

        self.child_birth_options = {
            'report_datetime': get_utcnow(),
            'first_name': 'TR',
            'initials': 'TT',
            'dob': get_utcnow(),
            'gender': MALE

        }

    def test_cage_aid_required(self):
        self.maternal_dataset_options['delivdt'] = get_utcnow(
        ) - relativedelta(years=15, months=2)
        self.maternal_dataset_options['protocol'] = 'Tshipidi'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=15, months=2),
            **self.child_dataset_options)
        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='1',
            child_version='1', )

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            hiv_testing=YES,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(),)

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent.subject_identifier,
            dob=(get_utcnow() - relativedelta(years=15, months=2)).date(),
            identity=caregiver_child_consent.identity,
            confirm_identity=caregiver_child_consent.identity,
            version=subject_consent.version)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        schedule_enrol_helper = ChildFollowUpEnrolmentHelper(
            subject_identifier=caregiver_child_consent.subject_identifier)
        schedule_enrol_helper.activate_child_fu_schedule()

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='3000',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childcageaid',
                subject_identifier=caregiver_child_consent.subject_identifier,
                visit_code='3000').entry_status, REQUIRED)

    def test_cage_aid_not_required(self):
        self.maternal_dataset_options['delivdt'] = get_utcnow(
        ) - relativedelta(years=10, months=6)
        self.maternal_dataset_options['protocol'] = 'Tshipidi'

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        self.child_dataset_options['infant_hiv_exposed'] = 'Unexposed'

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=10, months=6),
            **self.child_dataset_options)
        mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='1',
            child_version='1', )

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            biological_caregiver=YES,
            hiv_testing=YES,
            **self.options)

        caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            study_child_identifier=child_dataset.study_child_identifier,
            child_dob=maternal_dataset_obj.delivdt.date(),)

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent.subject_identifier,
            dob=(get_utcnow() - relativedelta(years=10, months=6)).date(),
            identity=caregiver_child_consent.identity,
            confirm_identity=caregiver_child_consent.identity,
            version=subject_consent.version)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2001',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        schedule_enrol_helper = ChildFollowUpEnrolmentHelper(
            subject_identifier=caregiver_child_consent.subject_identifier)
        schedule_enrol_helper.activate_child_fu_schedule()

        mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='3000',
                subject_identifier=caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childcageaid',
                subject_identifier=caregiver_child_consent.subject_identifier,
                visit_code='3000').entry_status, NOT_REQUIRED)
