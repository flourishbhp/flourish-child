from django.contrib import admin

from ..admin_site import flourish_child_admin
from ..forms import InfantFeedingForm
from ..models import InfantFeeding
from .model_admin_mixins import ChildCrfModelAdminMixin


@admin.register(InfantFeeding, site=flourish_child_admin)
class InfantFeedingAdmin(ChildCrfModelAdminMixin, admin.ModelAdmin):

    form = InfantFeedingForm
    fieldsets = (
        (None, {
            'fields': [
                "child_visit",
                "report_datetime",
                "last_att_sche_visit",
                "other_feeding",
                "formula_intro_occur",
                "formula_intro_date",
                "took_formula",
                "is_first_formula",
                "date_first_formula",
                "est_date_first_formula",
                "water",
                "juice",
                "cow_milk",
                "cow_milk_yes",
                "other_milk",
                "other_milk_animal",
                "milk_boiled",
                "fruits_veg",
                "cereal_porridge",
                "solid_liquid",
                "rehydration_salts",
                "water_used",
                "water_used_other",
                "ever_breastfeed",
                "complete_weaning",
                "weaned_completely",
                "most_recent_bm",
                "times_breastfed",
                "comments"]
        }),)
    readonly_fields = ('last_att_sche_visit',)
    radio_fields = {
        "other_feeding": admin.VERTICAL,
        "formula_intro_occur": admin.VERTICAL,
        "water_used": admin.VERTICAL,
        "took_formula": admin.VERTICAL,
        "is_first_formula": admin.VERTICAL,
        "est_date_first_formula": admin.VERTICAL,
        "water": admin.VERTICAL,
        "juice": admin.VERTICAL,
        "cow_milk": admin.VERTICAL,
        "cow_milk_yes": admin.VERTICAL,
        "other_milk": admin.VERTICAL,
        "milk_boiled": admin.VERTICAL,
        "fruits_veg": admin.VERTICAL,
        "cereal_porridge": admin.VERTICAL,
        "solid_liquid": admin.VERTICAL,
        "rehydration_salts": admin.VERTICAL,
        "ever_breastfeed": admin.VERTICAL,
        "complete_weaning": admin.VERTICAL,
        "weaned_completely": admin.VERTICAL,
        "times_breastfed": admin.VERTICAL}
