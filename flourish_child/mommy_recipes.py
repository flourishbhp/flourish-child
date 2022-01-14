from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, ON_STUDY, YES, PARTICIPANT, NO
from edc_registration.models import RegisteredSubject
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, seq
from flourish_caregiver.models import ScreeningPriorBhpParticipants, \
    SubjectConsent
from .models import ChildDummySubjectConsent, ChildDataset, ChildAssent, \
    ChildVisit, ChildBirth
from .models import ChildGadAnxietyScreening, ChildPhqDepressionScreening, \
    ChildSocioDemographic
from flourish_child.models.birth_data import BirthData

fake = Faker()

childdummysubjectconsent = Recipe(
    ChildDummySubjectConsent,
    subject_identifier=None,
    version='1'
)

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
    remain_in_study=YES,
)

# TODO
# Recipe for child birth
# throws an error: CaregiverChildConsent matching query does not exist.
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

childbirth = Recipe(
    ChildBirth)

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
