from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from ..choices import POS_NEG_IND, YES_NO_UNCERTAIN


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

    gestational_age = models.IntegerField(
        verbose_name='What is the Gestational Age of your child/adolescent',
        null=True,
        blank=True)

    gestational_age_est = models.IntegerField(
        verbose_name='What is the Estimated Gestational Age of your '
                     'child/adolescent',
        null=True,
        blank=True)

    premature_at_birth = models.CharField(
        verbose_name='Was your child/adolescent premature when born?',
        choices=YES_NO_UNCERTAIN,
        max_length=3,
        help_text='Preterm birth is a birth that occurs before 37 weeks '
                  'gestation. ')

    child_hiv_docs = models.CharField(
        verbose_name='Is there documentation of the child’s HIV status?',
        choices=YES_NO,
        max_length=3, )

    child_hiv_result = models.CharField(
        verbose_name='HIV test result',
        choices=POS_NEG_IND,
        max_length=14)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'HUU Pre-Enrollment'
        verbose_name_plural = 'HUU Pre-Enrollment'
