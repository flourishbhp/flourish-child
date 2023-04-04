from django.urls.conf import path
from django.views.generic.base import RedirectView

from flourish_child.admin_site import flourish_child_admin
from .autocomple_view import get_received_dates

app_name = 'flourish_child'

urlpatterns = [
    path('admin/', flourish_child_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
    path('received_dates/<slug:vaccine>/', get_received_dates, name='received-dates'),
]
