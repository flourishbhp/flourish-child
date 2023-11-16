from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy
from edc_constants.constants import YES, NO
from edc_appointment.models import Appointment as MotherAppointment
from edc_visit_tracking.constants import SCHEDULED
from ..models import Appointment, ChildDummySubjectConsent
from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin
from flourish_caregiver.models import CaregiverChildConsent


@tag('child_relation')
class TestRelationshipFatherInvolvementGroups(TestCase):
    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=0),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Mpepu', }

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        self.child = mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(5, 1),
            **self.child_dataset_options)

        self.sh = SubjectHelperMixin()

        subject_identifier = self.sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        self.visit_2000M = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=MotherAppointment.objects.get(
                visit_code='2000M',
                subject_identifier=subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        child_consent = CaregiverChildConsent.objects.get(
            subject_consent__subject_identifier=subject_identifier
        )

        self.dummy_consent = ChildDummySubjectConsent.objects.get(
            subject_identifier=child_consent.subject_identifier)

        self.relationship_father_involment = mommy.make_recipe(
            'flourish_caregiver.relationshipfatherinvolvement',
            maternal_visit=self.visit_2000M,
            conunselling_referral=YES
        )

        self.visit_2000 = mommy.make_recipe(
            'flourish_child.childvisit',
            appointment=Appointment.objects.get(
                visit_code='2000',
                subject_identifier=self.dummy_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def year_3_age(self, year_3_years, year_3_months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=year_3_years,
                                                      months=year_3_months)
        return child_dob

    def test_child_social_work_required(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childsocialworkreferral',
                subject_identifier=self.dummy_consent.subject_identifier,
                visit_code='2000').entry_status, REQUIRED)

    def test_caregiver_social_work_not_required(self):

        self.relationship_father_involment.conunselling_referral = NO
        self.relationship_father_involment.save()

        self.visit_2000.save()

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_child.childsocialworkreferral',
                subject_identifier=self.dummy_consent.subject_identifier,
                visit_code='2000').entry_status, NOT_REQUIRED)
