from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, MALE, NO, NOT_APPLICABLE, ON_STUDY, \
    PARTICIPANT, POS, YES
from edc_registration.models import RegisteredSubject
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, seq

from flourish_caregiver.models import (CaregiverChildConsent,
                                       CaregiverPreviouslyEnrolled,
                                       RelationshipFatherInvolvement, ScreeningPregWomen,
                                       ScreeningPriorBhpParticipants,
                                       SubjectConsent, TbAdolConsent)
from flourish_child.models.adol_tb_referral import TbReferalAdol
from flourish_child.models.birth_data import BirthData
from flourish_child.models.child_phq_referral import ChildPhqReferral
from flourish_child.models.child_phq_referral_fu import ChildPhqReferralFU
from flourish_prn.models.tb_adol_off_study import TBAdolOffStudy
from .models import (ChildAssent, ChildBirth, ChildClinicalMeasurements, ChildDataset,
                     ChildDummySubjectConsent, ChildFoodSecurityQuestionnaire, ChildVisit,
                     HivTestingAdol, InfantDevScreening12Months,
                     InfantDevScreening18Months, InfantDevScreening36Months,
                     TbAdolAssent, TbAdolEngagement, TbAdolInterview, TbLabResultsAdol,
                     TbPresenceHouseholdMembersAdol, TbVisitScreeningAdolescent)

from .models import (ChildContinuedConsent, ChildGadAnxietyScreening,
                     ChildPhqDepressionScreening, ChildSocioDemographic, ChildTBReferral,
                     ChildTBScreening, InfantArvProphylaxis, InfantFeeding,
                     InfantHIVTestingAge6To8Weeks, InfantHIVTesting9Months,
                     InfantHIVTesting, InfantHIVTestingAfterBreastfeeding, ChildhoodLeadExposureRisk)

fake = Faker()

childdummysubjectconsent = Recipe(
    ChildDummySubjectConsent,
    subject_identifier=None,
    version='1'
)

screeningpregwomen = Recipe(
    ScreeningPregWomen,
    hiv_testing=YES,
    breastfeed_intent=YES)

childassent = Recipe(
    ChildAssent,
    subject_identifier=None,
    identity=seq('123476521'),
    confirm_identity=seq('123476521'),
    identity_type='OMANG',
    first_name=fake.first_name,
    last_name=fake.last_name,
    gender='M',
    hiv_testing=YES,
    remain_in_study=YES)

childbirth = Recipe(
    ChildBirth,
    report_datetime=get_utcnow(),
    first_name='AS',
    initials='AY',
    dob=get_utcnow(),
    gender='Male'
)

childdataset = Recipe(
    ChildDataset, )

registeredsubject = Recipe(
    RegisteredSubject,
    subject_identifier=None)

screeningpriorbhpparticipants = Recipe(
    ScreeningPriorBhpParticipants,
    child_alive=YES,
    flourish_participation='interested')

subjectconsent = Recipe(
    SubjectConsent,
    subject_identifier=None,
    consent_datetime=get_utcnow(),
    dob=get_utcnow() - relativedelta(years=25),
    first_name=fake.first_name,
    last_name=fake.last_name,
    initials='XX',
    gender='F',
    identity=seq('123425679'),
    confirm_identity=seq('123425679'),
    identity_type='OMANG',
    is_dob_estimated='-',
    version='1'
)

childvisit = Recipe(
    ChildVisit,
    report_datetime=get_utcnow(),
    reason=SCHEDULED,
    information_provider='MOTHER',
    study_status=ON_STUDY,
    survival_status=ALIVE,
    info_source=PARTICIPANT)

childsociodemographic = Recipe(
    ChildSocioDemographic,
    attend_school=YES)

birthdata = Recipe(
    BirthData,
    congenital_anomalities=YES)

caregiverchildconsent = Recipe(
    CaregiverChildConsent,
    first_name=fake.first_name,
    last_name=fake.last_name,
    subject_identifier='',
    gender='M',
    child_test=YES,
    child_dob=(get_utcnow() - relativedelta(years=3)).date(),
    child_remain_in_study=YES,
    child_preg_test=NOT_APPLICABLE,
    child_knows_status=YES,
    identity=seq('234513187'),
    identity_type='birth_cert',
    confirm_identity=seq('234513187')
)

childgadanxietyscreening = Recipe(
    ChildGadAnxietyScreening,
    feeling_anxious='1',
    control_worrying='3',
    worrying='1',
    trouble_relaxing='0',
    restlessness='1',
    easily_annoyed='2',
    fearful='3', )

childphqdeprscreening = Recipe(
    ChildPhqDepressionScreening,
    activity_interest='1',
    depressed='2',
    sleep_disorders='1',
    fatigued='1',
    eating_disorders='0',
    self_doubt='0',
    easily_distracted='1',
    restlessness='1',
    self_harm='4',
    self_harm_thoughts=NO,
    suidice_attempt=NO)

caregiverpreviouslyenrolled = Recipe(
    CaregiverPreviouslyEnrolled,
    report_datetime=get_utcnow(),
    maternal_prev_enroll=YES,
    current_hiv_status=POS,
    last_test_date=get_utcnow().date(),
    test_date=get_utcnow().date(),
    is_date_estimated=NO,
    sex=MALE,
    relation_to_child='Mother', )

infantdevscreening36months = Recipe(
    InfantDevScreening36Months,
    report_datetime=get_utcnow(),
    speaking=YES,
    hearing_specialist="blah blah",
    vision=YES,
    vision_specialist="blah blah",
    play_with_people=YES,
    play_with_toys=YES,
    cognitive_specialist="blah blah",
    runs_well=YES,
    self_feed=YES,
    motor_skills_specialist="blah blah",
    caregiver_concerns="blah blah"
)

infantdevscreening12months = Recipe(
    InfantDevScreening12Months,
    report_datetime=get_utcnow(),
    hearing=YES,
    hearing_response=YES,
    hearing_communication=YES,
    hearing_specialist="blah blah",
    eye_movement=YES,
    familiar_obj=YES,
    vision_specialist="blah blah",
    cognitive_behavior=YES,
    understands=YES,
    cognitive_specialist="blah blah",
    stands=YES,
    picks_objects=YES,
    motor_skills_specialist="blah blah",
    caregiver_concerns="blah blah"
)

infantdevscreening18months = Recipe(
    InfantDevScreening18Months,
    report_datetime=get_utcnow(),
    hearing=YES,
    hearing_more=YES,
    speaking_specialist=YES,
    vision=YES,
    vision_specialist="blah blah",
    cognitive_behavior=YES,
    cognitive_specialist="blah blah",
    walks=YES,
    self_feed=YES,
    caregiver_concerns="blah blah",
)

childfoodsecurityquestionnaire = Recipe(
    ChildFoodSecurityQuestionnaire,
    child_visit=None,
)

childphqreferral = Recipe(
    ChildPhqReferral, )

childphqreferralfu = Recipe(
    ChildPhqReferralFU)

tblabresultsadol = Recipe(
    TbLabResultsAdol)

tbadoloffstudy = Recipe(
    TBAdolOffStudy)

tbadolassent = Recipe(
    TbAdolAssent, )

tbvisitscreening = Recipe(
    TbVisitScreeningAdolescent, )

tbadolcaregiverconsent = Recipe(
    TbAdolConsent, )

hivtestingadol = Recipe(
    HivTestingAdol, )

tbpresencehouseholdmembersadol = Recipe(
    TbPresenceHouseholdMembersAdol, )

tbvisitscreeningadolescent = Recipe(
    TbVisitScreeningAdolescent, )

tbadolreferral = Recipe(
    TbReferalAdol)

tbadolinterview = Recipe(
    TbAdolInterview, )

tbadolengagement = Recipe(
    TbAdolEngagement)

childclinicalmeasurements = Recipe(
    ChildClinicalMeasurements, )

infantfeeding = Recipe(
    InfantFeeding,
)

infanthivtesting = Recipe(
    InfantHIVTesting
)

infantarvprophylaxis = Recipe(
    InfantArvProphylaxis
)
relationshipfatherinvolvement = Recipe(
    RelationshipFatherInvolvement,
)

childtbreferral = Recipe(
    ChildTBReferral,
)

childtbscreening = Recipe(
    ChildTBScreening,
)

infanthivtestingafterbreastfeeding = Recipe(
    InfantHIVTestingAfterBreastfeeding,
)

infanthivtestingage6to8weeks = Recipe(
    InfantHIVTestingAge6To8Weeks,
)

infanthivtesting9months = Recipe(
    InfantHIVTesting9Months,
)

childcontinuedconsent = Recipe(
    ChildContinuedConsent,
    first_name=fake.first_name,
    last_name=fake.last_name,
    identity=seq('123425679'),
    confirm_identity=seq('123425679'),
    identity_type='OMANG',
)

childhoodleadexposurerisk=Recipe(
ChildhoodLeadExposureRisk
)
