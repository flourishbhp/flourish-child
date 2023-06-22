from django.test import TestCase, tag
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from edc_base.utils import get_utcnow
from edc_constants.constants import YES,NEG,NO
from dateutil.relativedelta import relativedelta
from ..models import Appointment, ChildDummySubjectConsent
from edc_visit_tracking.constants import MISSED_VISIT,SCHEDULED
from django.apps import apps as django_apps

@tag('missedbirthvisit')
class TestMissedBirthVisit(TestCase):
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

    @tag('mbv')
    def test_missed_birth_visit_is_triggered(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            delivery_datetime=get_utcnow(),
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
                subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
                visit_code='2000D'),
            is_present=NO,
            report_datetime=get_utcnow(),
            reason=MISSED_VISIT)
        
        reference_model = 'flourish_prn.missedbirthvisit'
        missed_birth_visit_model_cls = django_apps.get_model(
            'edc_action_item.actionitem')
        
        self.assertTrue(missed_birth_visit_model_cls.objects.filter(subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,reference_model=reference_model).exists(),"Object Does Not exist")
    
        

    def test_missed_birth_visit_is_not_triggered(self):
        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            current_hiv_status=NEG,
            subject_identifier=self.preg_subject_consent.subject_identifier, )

        mommy.make_recipe(
            'flourish_caregiver.maternaldelivery',
            subject_identifier=self.preg_subject_consent.subject_identifier,
            delivery_datetime=get_utcnow(),
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
                subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,
                visit_code='2000D'),
            is_present=YES,
            report_datetime=get_utcnow(),
            reason=SCHEDULED)
        
        reference_model = 'flourish_prn.missedbirthvisit'
        missed_birth_visit_model_cls = django_apps.get_model(
            'edc_action_item.actionitem')
        
        self.assertFalse(missed_birth_visit_model_cls.objects.filter(subject_identifier=self.preg_caregiver_child_consent_obj.subject_identifier,reference_model=reference_model).exists(),"Object exist")
