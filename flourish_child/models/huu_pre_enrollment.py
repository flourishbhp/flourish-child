from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, GENDER

from ..choices import POS_NEG_IND, YES_NO_UNCERTAIN, YES_NO_UNKNOWN,\
                      UNCERTAIN_GEST_AGE


class HuuPreEnrollment(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, ], )

    screening_identifier = models.CharField(
        verbose_name='Eligibility Identifier',
        max_length=36,
        unique=True,
        editable=False)

    child_dob = models.DateField(
        verbose_name='What is your DOB?', )

    child_hiv_docs = models.CharField(
        verbose_name='Is there documentation of the child’s HIV status?',
        choices=YES_NO,
        max_length=3, )

    child_hiv_result = models.CharField(
        verbose_name='HIV test result',
        choices=POS_NEG_IND,
        max_length=14)

    weight = models.IntegerField(
        verbose_name='Weight (kg)')

    height = models.IntegerField(
        verbose_name='Height (cm)')

    sex = models.CharField(
        verbose_name='Sex',
        max_length=3,
        choices=GENDER)

    knows_gest_age = models.CharField(
        verbose_name='Does the caregiver know the gestational age of the '
                     'child?',
        max_length=3,
        choices=YES_NO)

    gestational_age = models.IntegerField(
        verbose_name='What is the Gestational Age of the child/adolescent?',
        null=True,
        blank=True,
        max_length=2,
        validators=[MaxValueValidator(42), MinValueValidator(24)])

    uncertain_gest_age = models.CharField(
        verbose_name='If the mother is uncertain of the gestational age of '
                     'this child, which statement is truest about this child’s'
                     ' gestational age?',
        choices=UNCERTAIN_GEST_AGE,
        max_length=12,
        null=True,
        blank=True)

    premature_at_birth = models.CharField(
        verbose_name='Was the child/adolescent premature when born?',
        choices=YES_NO_UNCERTAIN,
        max_length=3,
        help_text='Preterm birth is a birth that occurs before 37 weeks '
                  'gestation. You may have to ask the mother if this child was'
                  ' born earlier than she was told to expect the child, right '
                  'at the same time, or after.')

    breastfed = models.CharField(
        verbose_name='Was your child breastfed?',
        choices=YES_NO_UNKNOWN,
        max_length=8)

    months_breastfeed = models.IntegerField(
        verbose_name='Approximately how many months did this child breastfeed,'
                     ' including periods where the child was breast feeding '
                     'and taking formula and solid foods together?',
        validators=[MaxValueValidator(30), MinValueValidator(1)])

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'HUU Pre-Enrollment'
        verbose_name_plural = 'HUU Pre-Enrollment'
