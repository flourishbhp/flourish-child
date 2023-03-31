from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from .child_crf_model_mixin import ChildCrfModelMixin
from ..choices import GENDER_NA, MENARCHE_AVAIL, TANNER_STAGES


class ChildTannerStaging(ChildCrfModelMixin):

    """ A model completed by the user on tanner staging for infants 7 years or
        older at enrolment.
    """

    assessment_done = models.CharField(
        verbose_name='Was a tanner stage assessment performed?',
        max_length=3,
        choices=YES_NO)

    reasons_not_done = models.CharField(
        verbose_name='Why was tanner staging not performed?',
        max_length=25,
        null=True, blank=True)

    child_gender = models.CharField(
        verbose_name='Indicate participant gender',
        max_length=10,
        choices=GENDER_NA,
        default=NOT_APPLICABLE)

    breast_stage = models.CharField(
        verbose_name='What was the tanner stage for female breast',
        max_length=15,
        choices=TANNER_STAGES,
        default=NOT_APPLICABLE)

    pubic_hair_stage = models.CharField(
        verbose_name='What was the tanner stage for pubic hair',
        max_length=15,
        choices=TANNER_STAGES,
        default=NOT_APPLICABLE)

    manarche_dt_avail = models.CharField(
        verbose_name='Is the date of menarche available?',
        max_length=30,
        choices=MENARCHE_AVAIL,
        default=NOT_APPLICABLE)

    menarche_dt = models.DateField(
        verbose_name='Indicate the date of menarche',
        blank=True, null=True)

    menarche_dt_est = models.CharField(
        verbose_name='Is this date estimated',
        max_length=15,
        blank=True,
        null=True,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    male_gen_stage = models.CharField(
        verbose_name='What is the tanner stage for male genitalia',
        max_length=15,
        choices=TANNER_STAGES,
        default=NOT_APPLICABLE)

    testclr_vol_measrd = models.CharField(
        verbose_name='Was the testicular volume measured?',
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    rgt_testclr_vol = models.DecimalField(
        verbose_name='Indicate the testicular volume of right testicle',
        null=True, blank=True,
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(25)])

    lft_testclr_vol = models.DecimalField(
        verbose_name='Indicate the testicular volume of left testicle',
        null=True, blank=True,
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(25)])

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = 'Child Tanner Staging'
        verbose_name_plural = 'Child Tanner Staging'
