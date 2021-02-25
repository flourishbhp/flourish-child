from faker import Faker
from model_mommy.recipe import Recipe, seq
from .models import ChildDummySubjectConsent, ChildDataset, ChildAssent
from edc_registration.models import RegisteredSubject

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
)

childdataset = Recipe(
    ChildDataset,)

registeredsubject = Recipe(
    RegisteredSubject,
    subject_identifier=None)
