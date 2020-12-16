from faker import Faker
from model_mommy.recipe import Recipe

from .models import ChildDummySubjectConsent
from edc_registration.models import RegisteredSubject

fake = Faker()

childdummysubjectconsent = Recipe(
    ChildDummySubjectConsent,
    subject_identifier=None,
    version='1'
)

registeredsubject = Recipe(
    RegisteredSubject,
    subject_identifier=None)
