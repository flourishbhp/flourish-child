from django.contrib import admin

from flourish_prn.admin import ChildOffStudyAdmin
from ..admin_site import flourish_child_admin
from ..forms import TBAdolOffStudyForm
from ..models import TBAdolOffStudy


@admin.register(TBAdolOffStudy, site=flourish_child_admin)
class TBAdolOffStudyAdmin(ChildOffStudyAdmin, admin.ModelAdmin):
    form = TBAdolOffStudyForm
