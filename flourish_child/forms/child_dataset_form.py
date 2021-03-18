from django import forms
from edc_base.sites.forms import SiteModelFormMixin

from ..models import ChildDataset


class ChildDatasetForm(SiteModelFormMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    study_child_identifier = forms.CharField(
        label='Study Child Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    study_maternal_identifier = forms.CharField(
        label='Study Maternal Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_enrolldate = forms.CharField(
        label='Infant enrollment date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_randdt = forms.CharField(
        label='Date of infant randomization',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_sex = forms.CharField(
        label='Infant gender',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_azt_birth = forms.CharField(
        label='Infant started AZT',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_azt_days = forms.CharField(
        label='Duration of infant AZT (days)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_azt_startdate = forms.CharField(
        label='AZT start date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_azt_stopdate = forms.CharField(
        label='AZT stop date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_sdnvp_birth = forms.CharField(
        label='Infant received sdNVP',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_hiv_exposed = forms.CharField(
        label='Infant HIV exposure status',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_hiv_status = forms.CharField(
        label='Infant HIV infection status',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_breastfed = forms.CharField(
        label='Infant breastfed',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_breastfed_days = forms.CharField(
        label='Breastfeeding duration (days)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    weaned = forms.CharField(
        label='Weaning indicator',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    weandt = forms.CharField(
        label='Weaning date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    weancat = forms.CharField(
        label='Weaning by category',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    birthweight = forms.CharField(
        label='Birth weight (kg)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    birthwtcat = forms.CharField(
        label='Birth weight (kg) by category',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    height_0 = forms.CharField(
        label='Height (cm) at delivery',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    headcirc_0 = forms.CharField(
        label='Head circumference (cm) at delivery',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    apgarscore_1min = forms.CharField(
        label='APGAR score at 1min',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    apgarscore_5min = forms.CharField(
        label='APGAR score at 5min',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    apgarscore_10min = forms.CharField(
        label='APGAR score at 10min',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    low_birthweight = forms.CharField(
        label='Infant born low birth weight',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_premature = forms.CharField(
        label='Infant born premature (<37 weeks)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    height_6mo = forms.CharField(
        label='Height (cm) at 6 months',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    height_18mo = forms.CharField(
        label='Height (cm) at 18 months',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    height_24mo = forms.CharField(
        label='Height (cm) at 24 months',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    headcirc_18mo = forms.CharField(
        label='Head circumference (cm) at 18 months',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    headcirc_24mo = forms.CharField(
        label='Head circumference (cm) at 24 months',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    weight_18mo = forms.CharField(
        label='Weight (kg) at 18 months',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    weight_24mo = forms.CharField(
        label='Weight (kg) at 18 months',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_vitalstatus_final = forms.CharField(
        label='Final infant vital status',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    deathdt = forms.CharField(
        label='Death date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    deathcause = forms.CharField(
        label='Cause of death',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    firsthospdt = forms.CharField(
        label='Date of first hospitalization',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    hospnum = forms.CharField(
        label='Number of times hospitalized',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    idth = forms.CharField(
        label='Infant death indicator (0= censored)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    idth_days = forms.CharField(
        label='Days from infant birth to death (censored)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    ihiv = forms.CharField(
        label='Indicator of HIV endpoint (0=censored)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    ihiv_days = forms.CharField(
        label='Time to HIV endpoint (days from birth)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    ihosp = forms.CharField(
        label='Infant hospitalization indicator (0= censored)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    ihosp_days = forms.CharField(
        label='Days from infant birth to first hospitalization (censored)',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_bcg = forms.CharField(
        label='BCG vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_dtap = forms.CharField(
        label='DTAP vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_hbv = forms.CharField(
        label='HBV vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_hiv = forms.CharField(
        label='HIV vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_measles = forms.CharField(
        label='Measles vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_mmr = forms.CharField(
        label='MMR vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_pneum = forms.CharField(
        label='Pneumoccal vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_polio = forms.CharField(
        label='Polio vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infantvacc_rota = forms.CharField(
        label='Rotavirus vaccine received?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_offstudydate = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_lastcontactdt = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_onstudy_days = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_offstudy_reason = forms.CharField(
        label='Days infant on-study',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    curr_age = forms.CharField(
        label='Current Age',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    age_gt17_5 = forms.CharField(
        label='Age greater than 17.5',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    infant_offstudy_complete = forms.CharField(
        label='Infant Offstudy Complete',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    offstrs = forms.CharField(
        label='Offstrs',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    offstcd = forms.CharField(
        label='Offstcd',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ChildDataset
        fields = '__all__'
