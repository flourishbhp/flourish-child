import ast

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import Group, User
from django.core import mail
from django.test import tag, TestCase
from django.test.client import RequestFactory
from edc_base import get_utcnow
from edc_constants.constants import MALE, YES
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from flourish_calendar.models import Reminder
from flourish_child.models import ChildClinicalMeasurements
from flourish_child.models.child_appointment import Appointment
from pre_flourish.helper_classes import MatchHelper
from pre_flourish.models import MatrixPool


@tag('heu_huu_match_emails')
class TestHEUHUUMatchEmails(TestCase):
    def setUp(self):
        import_holidays()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='nmunatsi@bhp.org.bw')
        self.group = Group.objects.create(name='pre_flourish')
        self.group.user_set.add(self.user)
        self.study_maternal_identifier = '1234'
        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=12, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=get_utcnow() - relativedelta(years=12, months=5),
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',
            screening_identifier=maternal_dataset_obj.screening_identifier, )

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=maternal_dataset_obj.screening_identifier,
            breastfeed_intent=YES,
            **self.options)

        self.caregiver_child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            gender=MALE,
            study_child_identifier=self.child_dataset_options['study_child_identifier'],
            child_dob=maternal_dataset_obj.delivdt, )

        mommy.make_recipe(
            'flourish_child.childassent',
            subject_identifier=self.caregiver_child_consent.subject_identifier,
            first_name=self.caregiver_child_consent.first_name,
            last_name=self.caregiver_child_consent.last_name,
            dob=self.caregiver_child_consent.child_dob,
            identity=self.caregiver_child_consent.identity,
            confirm_identity=self.caregiver_child_consent.identity,
            remain_in_study=YES,
            version=self.caregiver_child_consent.version)

        mommy.make_recipe(
            'flourish_caregiver.caregiverpreviouslyenrolled',
            subject_identifier=self.subject_consent.subject_identifier)

        self.child_visit = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=self.caregiver_child_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.bmi_group = '>18'
        self.age_range = '(9.5, 13)'
        self.gender = 'female'
        self.subject_identifiers = '[\'123\', \'456\']'
        self.matrix_pool = MatrixPool.objects.create(
            pool='huu', bmi_group=self.bmi_group, age_group=self.age_range,
            gender_group=self.gender, count=2)
        self.matrix_pool.set_subject_identifiers(self.subject_identifiers)
        self.matrix_pool.save()

        self.match_helper = MatchHelper()

    def test_child_clinical_measurements_on_post_save(self):
        """Test that an email is sent to pre_flourish users when a child clinical
        measurement is saved."""
        instance = ChildClinicalMeasurements.objects.create(
            child_visit=self.child_visit,
            child_weight_kg=65,
            child_height=180,
            is_child_preg=YES,
            child_muac=30,
        )
        instance.save()

        self.assertGreaterEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reminder: Enroll into Flourish')

    def test_send_email_to_pre_flourish_users(self):
        huu_matrix_group = [self.matrix_pool]

        self.match_helper.send_email_to_pre_flourish_users(huu_matrix_group)

        self.assertGreaterEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reminder: Enroll into Flourish')

        self.assertIn('Subject Identifier(s):\n[\'123', mail.outbox[0].body)

    def test_create_reminder(self):
        """Test that a reminder is created when a new child clinical
        measurement is saved."""
        huu_matrix_group = [self.matrix_pool]

        self.match_helper.send_email_to_pre_flourish_users(huu_matrix_group)

        self.assertNotEquals(0, Reminder.objects.filter(
            title='Reminder: Enroll into Flourish').count())

    @tag('eesa')
    def test_create_new_matrix_pool(self):
        """Test that a new matrix pool is created when a new child clinical
        measurement is saved."""
        self.bmi_group = '<14.9'
        self.age_range = '(9.5, 13)'
        self.gender = 'female'
        subject_identifier = self.child_visit.subject_identifier
        self.matrix_pool = MatrixPool.objects.create(
            pool='heu', bmi_group=self.bmi_group, age_group=self.age_range,
            gender_group=self.gender, count=2)
        huu_matrix_pool = MatrixPool.objects.create(
            pool='huu', bmi_group='15-17.9', age_group=self.age_range,
            gender_group=self.gender, count=2,
            subject_identifiers=self.subject_identifiers)
        huu_matrix_pool.save()
        subject_identifiers = ast.literal_eval(self.subject_identifiers)
        subject_identifiers.append(self.child_visit.subject_identifier)
        self.matrix_pool.set_subject_identifiers(subject_identifiers)
        self.matrix_pool.save()

        self.assertGreaterEqual(MatrixPool.objects.all().count(), 1)

        string = MatrixPool.objects.get(
            pool='heu', bmi_group=self.bmi_group, age_group=self.age_range,
            gender_group=self.gender).subject_identifiers
        substring = self.child_visit.subject_identifier
        self.assertIn(substring, string)

        instance = ChildClinicalMeasurements.objects.create(
            child_visit=self.child_visit,
            child_weight_kg=15,
            child_height=93,
            is_child_preg=YES,
            child_muac=30,
        )
        instance.save()

        bmi = instance.child_weight_kg / ((instance.child_height / 100) ** 2)
        bmi_group = self.match_helper.bmi_group(bmi)

        second_matrix_pool_obj = MatrixPool.objects.get(
            pool='heu', bmi_group=bmi_group, age_group=self.age_range,
            gender_group=self.gender)
        self.assertTrue(subject_identifier in
                        second_matrix_pool_obj.get_subject_identifiers)
        self.assertEqual(second_matrix_pool_obj.count, 1)

        self.assertGreaterEqual(MatrixPool.objects.all().count(), 2)

        first_matrix_pool_obj = MatrixPool.objects.get(
            pool='heu', bmi_group=self.bmi_group, age_group=self.age_range,
            gender_group=self.gender)

        string = first_matrix_pool_obj.subject_identifiers
        self.assertNotIn(subject_identifier, string)
        self.assertEqual(first_matrix_pool_obj.count, 1)
