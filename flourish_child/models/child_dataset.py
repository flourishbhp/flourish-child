from django.db import models
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin


class ChildDataset(
        NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):

    study_child_identifier = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Study Child Subject Identifier')

    study_maternal_identifier = models.CharField(
        verbose_name="Study maternal Subject Identifier",
        max_length=50)

    first_name = FirstnameField(
        verbose_name='Firstname',
        null=True, blank=False)

    last_name = LastnameField(null=True, blank=False)

    dob = models.DateField(null=True, blank=True)

    infant_enrolldate = models.DateField(
        verbose_name='Infant enrollment date')

    infant_randdt = models.DateField(
        verbose_name='Date of infant randomization',
        blank=True, null=True)

    infant_sex = models.CharField(
        verbose_name='Infant gender',
        max_length=7)

    infant_azt_birth = models.CharField(
        verbose_name='Infant started AZT',
        max_length=3)

    infant_azt_days = models.IntegerField(
        verbose_name='Duration of infant AZT (days)',
        blank=True, null=True)

    infant_azt_startdate = models.DateField(
        verbose_name='AZT start date',
        blank=True, null=True)

    infant_azt_stopdate = models.DateField(
        verbose_name='AZT stop date',
        blank=True, null=True)

    infant_sdnvp_birth = models.CharField(
        verbose_name='Infant received sdNVP',
        max_length=3)

    infant_hiv_exposed = models.CharField(
        verbose_name='Infant HIV exposure status',
        max_length=150)

    infant_hiv_status = models.CharField(
        verbose_name='Infant HIV infection status',
        max_length=150)

    infant_breastfed = models.CharField(
        verbose_name='Infant breastfed',
        max_length=150)

    infant_breastfed_days = models.IntegerField(
        verbose_name='Breastfeeding duration (days)',
        blank=True, null=True)

    weaned = models.CharField(
        verbose_name='Weaning indicator',
        max_length=150, blank=True, null=True)

    weandt = models.DateField(
        verbose_name='Weaning date',
        blank=True, null=True)

    weancat = models.CharField(
        verbose_name='Weaning by category',
        max_length=150, blank=True, null=True)

    birthweight = models.DecimalField(
        verbose_name='Birth weight (kg)',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    birthwtcat = models.CharField(
        verbose_name='Birth weight (kg) by category',
        max_length=150, blank=True, null=True)

    height_0 = models.DecimalField(
        verbose_name='Height (cm) at delivery',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    headcirc_0 = models.DecimalField(
        verbose_name='Head circumference (cm) at delivery',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    apgarscore_1min = models.IntegerField(
        verbose_name='APGAR score at 1min',
        blank=True, null=True)

    apgarscore_5min = models.IntegerField(
        verbose_name='APGAR score at 5min',
        blank=True, null=True)

    apgarscore_10min = models.IntegerField(
        verbose_name='APGAR score at 10min',
        blank=True, null=True)

    low_birthweight = models.CharField(
        verbose_name='Infant born low birth weight',
        max_length=150)

    infant_premature = models.CharField(
        verbose_name='Infant born premature (<37 weeks)',
        max_length=150, blank=True, null=True)

    height_6mo = models.DecimalField(
        verbose_name='Height (cm) at 6 months',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    height_18mo = models.DecimalField(
        verbose_name='Height (cm) at 18 months',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    height_24mo = models.DecimalField(
        verbose_name='Height (cm) at 24 months',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    headcirc_18mo = models.DecimalField(
        verbose_name='Head circumference (cm) at 18 months',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    headcirc_24mo = models.DecimalField(
        verbose_name='Head circumference (cm) at 24 months',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    weight_18mo = models.DecimalField(
        verbose_name='Weight (kg) at 18 months',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    weight_24mo = models.DecimalField(
        verbose_name='Weight (kg) at 18 months',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    infant_vitalstatus_final = models.CharField(
        verbose_name='Final infant vital status',
        max_length=150)

    deathdt = models.DateField(
        verbose_name='Death date',
        blank=True, null=True)

    deathcause = models.CharField(
        verbose_name='Cause of death',
        max_length=150, blank=True, null=True)

    firsthospdt = models.DateField(
        verbose_name='Date of first hospitalization',
        blank=True, null=True)

    hospnum = models.IntegerField(
        verbose_name='Number of times hospitalized',
        blank=True, null=True)

    idth = models.IntegerField(
        verbose_name='Infant death indicator (0= censored)',
        blank=True, null=True)

    idth_days = models.IntegerField(
        verbose_name='Days from infant birth to death (censored)',
        blank=True, null=True)

    ihiv = models.IntegerField(
        verbose_name='Indicator of HIV endpoint (0=censored)',
        blank=True, null=True)

    ihiv_days = models.IntegerField(
        verbose_name='Time to HIV endpoint (days from birth)',
        blank=True, null=True)

    ihosp = models.IntegerField(
        verbose_name='Infant hospitalization indicator (0= censored)',
        blank=True, null=True)

    ihosp_days = models.IntegerField(
        verbose_name='Days from infant birth to first hospitalization (censored)',
        blank=True, null=True)

    infantvacc_bcg = models.CharField(
        verbose_name='BCG vaccine received?',
        max_length=150, blank=True, null=True)

    infantvacc_dtap = models.CharField(
        verbose_name='DTAP vaccine received?',
        max_length=150, blank=True, null=True)

    infantvacc_hbv = models.CharField(
        verbose_name='HBV vaccine received?',
        max_length=150, blank=True, null=True)

    infantvacc_hiv = models.CharField(
        verbose_name='HIV vaccine received?',
        max_length=150, blank=True, null=True)

    infantvacc_measles = models.CharField(
        verbose_name='Measles vaccine received?',
        max_length=150, blank=True, null=True)

    infantvacc_mmr = models.CharField(
        verbose_name='MMR vaccine received?',
        max_length=150, blank=True, null=True)

    infantvacc_pneum = models.CharField(
        verbose_name='Pneumoccal vaccine received?',
        max_length=150, blank=True, null=True)

    infantvacc_polio = models.CharField(
        verbose_name='Polio vaccine received?',
        max_length=150, blank=True, null=True)

    infantvacc_rota = models.CharField(
        verbose_name='Rotavirus vaccine received?',
        max_length=150, blank=True, null=True)

    infant_offstudydate = models.DateField(
        blank=True, null=True)

    infant_lastcontactdt = models.DateField(
        blank=True, null=True)

    infant_onstudy_days = models.IntegerField(
        blank=True, null=True)

    infant_offstudy_reason = models.CharField(
        verbose_name='Days infant on-study',
        max_length=200)

    curr_age = models.DecimalField(
        verbose_name='Current Age',
        decimal_places=2, max_digits=10,
        blank=True, null=True)

    age_gt17_5 = models.IntegerField(
        verbose_name='Age greater than 17.5')

    infant_offstudy_complete = models.IntegerField(
        verbose_name='Infant Offstudy Complete')

    # today = models.DateField(
    #     blank=True, null=True)

    offstrs = models.CharField(
        verbose_name='Offstrs',
        max_length=150,
        blank=True,
        null=True)

    offstcd = models.CharField(
        verbose_name='Offstcd',
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_child'
        verbose_name = 'Infant Dataset'
