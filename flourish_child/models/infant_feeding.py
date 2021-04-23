from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNSURE_NA
from edc_constants.constants import NOT_APPLICABLE

from ..choices import COWS_MILK, TIMES_BREASTFED, WATER_USED
from .child_crf_model_mixin import ChildCrfModelMixin


class InfantFeeding(ChildCrfModelMixin):

    """ A model completed by the user on the infant's feeding. """

    last_att_sche_visit = models.DateField(
        verbose_name=("When was the last attended scheduled visit where an "
                      "infant feeding form was completed? "),
        blank=True,
        null=True)

    other_feeding = models.CharField(
        verbose_name=("Since the last attended scheduled visit where an infant"
                      " feeding form was completed, has the child received any"
                      " liquids other than breast-milk? "),
        max_length=3,
        choices=YES_NO,
        help_text="If Formula Feeding or received any other foods or liquids "
                  "answer YES.")

    formula_intro_occur = models.CharField(
        verbose_name=(
            "Since the last attended scheduled visit has the child received "
            "any solid foods?"),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    formula_intro_date = models.DateField(
        verbose_name=("Date the infant participant first started receiving "
                      "solids since the last attended scheduled visit where "
                      "an infant feeding form was completed"),
        blank=True,
        null=True)

    took_formula = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed did the participant take "
                     "Formula?",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        help_text="If formula feeding since last visit answer YES",
        default=NOT_APPLICABLE)

    is_first_formula = models.CharField(
        verbose_name="Is this the first reporting of infant formula use?",
        max_length=15,
        choices=YES_NO,
        blank=True,
        null=True,)

    date_first_formula = models.DateField(
        verbose_name="Date infant formula introduced?",
        validators=[date_not_future, ],
        blank=True,
        null=True,
        help_text="provide date if this is first reporting of infant formula")

    est_date_first_formula = models.CharField(
        verbose_name="Is date infant formula introduced estimated?",
        max_length=15,
        choices=YES_NO,
        blank=True,
        null=True,
        help_text="provide date if this is first reporting of infant formula")

    water = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed did the participant take "
                     "Water?",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        help_text="Not as part of formula milk",
        default=NOT_APPLICABLE)

    juice = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed did the participant take "
                     "Juice?",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        help_text="If you answered YES to Q3 you must answer YES, NO or NOT "
                  "SURE to this question, you may not answer \'Not "
                  "Applicable\'.",
        default=NOT_APPLICABLE)

    cow_milk = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed did the participant take "
                     "Cow's milk?",
        max_length=15,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    cow_milk_yes = models.CharField(
        verbose_name="If 'Yes', cow's milk was...",
        max_length=25,
        choices=COWS_MILK,
        default=NOT_APPLICABLE)

    other_milk = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed did the participant take "
                     "Other animal milk?",
        max_length=15,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    other_milk_animal = OtherCharField(
        verbose_name="If 'Yes' specify which animal:",
        max_length=35,
        blank=True,
        null=True)

    milk_boiled = models.CharField(
        verbose_name="Was milk boiled?",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    fruits_veg = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed "
                     "did the participant take Fruits/vegetables",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    cereal_porridge = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed "
                     "did the participant take Cereal/porridge?",
        max_length=12,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    solid_liquid = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed did the participant take "
                     "Other solids and liquids",
        max_length=10,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    rehydration_salts = models.CharField(
        verbose_name="Since the last attended scheduled visit where an infant"
                     " feeding form was completed did the participant take "
                     "Oral rehydaration salts",
        max_length=12,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE)

    water_used = models.CharField(
        verbose_name="What water do you usually use to prepare the "
                     "participant's milk?",
        max_length=50,
        choices=WATER_USED,
        default=NOT_APPLICABLE)

    water_used_other = OtherCharField(
        verbose_name="If 'other', specify",
        max_length=35,
        blank=True,
        null=True)

    ever_breastfeed = models.CharField(
        verbose_name="Since the last attended scheduled visit,did the infant "
                     "ever breast-feed",
        max_length=3,
        choices=YES_NO)

    complete_weaning = models.CharField(
        verbose_name="If 'NO', did complete weaning from breast milk take "
                     "place before the last attended scheduled visit?",
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    weaned_completely = models.CharField(
        verbose_name=("Is the participant currently completely weaned from "
                      "breast milk (at least 72 hours without breast "
                      "feeding,no intention to re-start)?"),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    most_recent_bm = models.DateField(
        verbose_name="Date of most recent breastfeeding ",
        blank=True,
        null=True)

    times_breastfed = models.CharField(
        max_length=50,
        verbose_name=("Between the last attended scheduled visit where an "
                      "infant feeding form was completed and date of most "
                      "recent breastfeeding,how often did the participant "
                      "receive breast milk for feeding?"),
        choices=TIMES_BREASTFED,
        default=NOT_APPLICABLE)

    comments = models.TextField(
        max_length=200,
        verbose_name="List any comments about participant's feeding that are "
                     "not answered above",
        blank=True,
        null=True)

    def save(self, *args, **kwargs):
        previous_infant_feeding = self.previous_infant_feeding(self.infant_visit)
        if previous_infant_feeding:
            self.last_att_sche_visit = previous_infant_feeding.report_datetime.date()
        super(InfantFeeding, self).save(*args, **kwargs)

    def previous_infant_feeding(self, infant_visit):
        """ Return previous infant feeding from. """

        return self.__class__.objects.filter(
            infant_visit__appointment__subject_identifier=infant_visit.appointment.subject_identifier,
            report_datetime__lt=self.report_datetime).order_by(
                '-report_datetime').first()

    class Meta(ChildCrfModelMixin.Meta):
        app_label = 'flourish_child'
        verbose_name = "Infant Feeding Practices"
        verbose_name_plural = "Infant Feeding Practices"
