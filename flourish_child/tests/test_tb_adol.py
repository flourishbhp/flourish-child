from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import tag, TestCase
from edc_action_item import site_action_items
from edc_base import get_utcnow
from edc_constants.constants import NEG, NEW, NO, NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_schedule.models import SubjectScheduleHistory
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_child.models import Appointment, OnScheduleTbAdolFollowupSchedule
from flourish_prn.models.tb_adol_off_study import TBAdolOffStudy


@tag('tb-offstudy')
class TestTBAdol(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '2'}

        maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=15, months=2),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '12345',
            'protocol': 'Mashi',
            'preg_pi': 1}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Unexposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '12345',
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=15, months=2),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **maternal_dataset_options)

        self.flourish_consent_version = mommy.make_recipe(
            'flourish_caregiver.flourishconsentversion',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            version='2',
            child_version='2')

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            subject_identifier=maternal_dataset_obj.subject_identifier, )

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=NOT_APPLICABLE,
            **self.options)

        screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpriorbhpparticipants')

        screening_obj = screening_cls.objects.get(
            screening_identifier=self.subject_consent.screening_identifier)

        screening_obj.subject_identifier = self.subject_consent.subject_identifier

        screening_obj.save()

        caregiver_child_consent_obj = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            study_child_identifier=self.child_dataset_options.get(
                'study_child_identifier'),
            identity='126513789',
            confirm_identity='126513789',
            child_dob=(get_utcnow() - relativedelta(years=15, months=2)).date(), )
        caregiver_child_consent_obj.version = '2'
        caregiver_child_consent_obj.save()

        self.child_subject_identifier = caregiver_child_consent_obj.subject_identifier

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=self.subject_consent.subject_identifier)

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=caregiver_child_consent_obj.subject_identifier,
            dob=(get_utcnow() - relativedelta(years=10, months=2)).date(),
            identity=caregiver_child_consent_obj.identity,
            confirm_identity=caregiver_child_consent_obj.identity,
            version=self.subject_consent.version)

        self.data = {
            'citizen': YES,
            'tb_testing': YES,
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES
        }

        mommy.make_recipe(
            'flourish_child.tbadolassent',
            dob=(get_utcnow() - relativedelta(years=15, months=2)).date(),
            subject_identifier=self.child_subject_identifier,
            **self.data)

        self.child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2100A',
                subject_identifier=self.child_subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_create_off_study_action_lab_result(self):

        mommy.make_recipe(
            'flourish_child.adoltblabresults',
            quantiferon_result=NEG,
            child_visit=self.child_visit, )
        action_cls = site_action_items.get(TBAdolOffStudy.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.child_subject_identifier,
                action_type__name=TBAdolOffStudy.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item not created')

    def test_create_off_study_action_hiv_testing(self):

        mommy.make_recipe(
            'flourish_child.hivtestingadol',
            last_result=NEG,
            child_visit=self.child_visit, )

        action_cls = site_action_items.get(TBAdolOffStudy.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.child_subject_identifier,
                action_type__name=TBAdolOffStudy.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item not created')

    def test_create_off_study_action_adol_tb_presence(self):

        mommy.make_recipe(
            'flourish_child.tbpresencehouseholdmembersadol',
            tb_referral=YES,
            child_visit=self.child_visit, )

        action_cls = site_action_items.get(TBAdolOffStudy.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.child_subject_identifier,
                action_type__name=TBAdolOffStudy.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item not created')

    def test_create_off_study_action_tb_visit_screening_cough_duration(self):

        mommy.make_recipe(
            'flourish_child.tbvisitscreeningadolescent',
            cough_duration=NO,
            child_visit=self.child_visit, )

        action_cls = site_action_items.get(TBAdolOffStudy.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.child_subject_identifier,
                action_type__name=TBAdolOffStudy.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item not created')

    def test_create_off_study_action_tb_visit_screening_fever_duration(self):

        mommy.make_recipe(
            'flourish_child.tbvisitscreeningadolescent',
            fever_duration=NO,
            child_visit=self.child_visit, )

        action_cls = site_action_items.get(TBAdolOffStudy.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.child_subject_identifier,
                action_type__name=TBAdolOffStudy.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item not created')

    def test_create_off_study_action_tb_visit_screening_night_sweats(self):

        mommy.make_recipe(
            'flourish_child.tbvisitscreeningadolescent',
            night_sweats=NO,
            child_visit=self.child_visit, )

        action_cls = site_action_items.get(TBAdolOffStudy.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.child_subject_identifier,
                action_type__name=TBAdolOffStudy.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item not created')

    def test_create_off_study_action_tb_visit_screening_weight_loss(self):

        mommy.make_recipe(
            'flourish_child.tbvisitscreeningadolescent',
            weight_loss=NO,
            child_visit=self.child_visit, )

        action_cls = site_action_items.get(TBAdolOffStudy.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.child_subject_identifier,
                action_type__name=TBAdolOffStudy.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            self.fail('Action Item not created')

    def test_tb_adol_off_study(self):
        schedule_history = SubjectScheduleHistory.objects.get(
            schedule_name='tb_adol_schedule',
            onschedule_model='flourish_child.onschedulechildtbadolschedule',
            subject_identifier=self.child_subject_identifier
        )

        self.assertIsNone(schedule_history.offschedule_datetime)

        mommy.make_recipe(
            'flourish_child.tbadoloffstudy',
            subject_identifier=self.child_subject_identifier, )

        schedule_history = SubjectScheduleHistory.objects.get(
            schedule_name='tb_adol_schedule',
            onschedule_model='flourish_child.onschedulechildtbadolschedule',
            subject_identifier=self.child_subject_identifier
        )
        self.assertIsNotNone(schedule_history.offschedule_datetime)

    def test_puts_on_followup_schedule(self):
        """Asserts that the subject is put on the followup schedule."""
        mommy.make_recipe(
            'flourish_prn.tbadolreferral',
            subject_identifier=self.child_subject_identifier, )
        self.assertEqual(
            OnScheduleTbAdolFollowupSchedule.objects.filter(
                subject_identifier=self.child_subject_identifier).count(), 1)

    def test_tb_interview_transcription_rule_group(self):
        """Asserts the tb adolescent interview transcription crf is required if the
        interview language is  not none."""

        mommy.make_recipe(
            'flourish_prn.tbadolreferral',
            subject_identifier=self.child_subject_identifier, )

        self.child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2200A',
                subject_identifier=self.child_subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.tbadolinterviewtranslation',
            subject_identifier=self.child_subject_identifier,
            visit_code='2200A').entry_status, NOT_REQUIRED)

        mommy.make_recipe(
            'flourish_child.tbadolinterview',
            child_visit=self.child_visit,
            interview_language='None'
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.tbadolinterviewtranscription',
            subject_identifier=self.child_subject_identifier,
            visit_code='2200A').entry_status, REQUIRED)

    def test_tb_interview_translation_rule_group(self):
        """Asserts the tb adolescent interview translation crf is required if the
        interview language is setswana or both."""

        mommy.make_recipe(
            'flourish_prn.tbadolreferral',
            subject_identifier=self.child_subject_identifier, )

        self.child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2200A',
                subject_identifier=self.child_subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.tbadolinterviewtranslation',
            subject_identifier=self.child_subject_identifier,
            visit_code='2200A').entry_status, NOT_REQUIRED)

        mommy.make_recipe(
            'flourish_child.tbadolinterview',
            child_visit=self.child_visit,
            interview_language='both'
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.tbadolinterviewtranslation',
            subject_identifier=self.child_subject_identifier,
            visit_code='2200A').entry_status, REQUIRED)

    def test_tb_interview_rule_group(self):
        """Asserts the tb adolescent interview crf is required if
        interview_consent is YES."""

        mommy.make_recipe(
            'flourish_prn.tbadolreferral',
            subject_identifier=self.child_subject_identifier, )

        self.child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2200A',
                subject_identifier=self.child_subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.tbadolinterview',
            subject_identifier=self.child_subject_identifier,
            visit_code='2200A').entry_status, NOT_REQUIRED)

        mommy.make_recipe(
            'flourish_child.tbadolengagement',
            child_visit=self.child_visit,
            interview_consent=YES
        )

        self.assertEqual(CrfMetadata.objects.get(
            model='flourish_child.tbadolinterview',
            subject_identifier=self.child_subject_identifier,
            visit_code='2200A').entry_status, REQUIRED)
