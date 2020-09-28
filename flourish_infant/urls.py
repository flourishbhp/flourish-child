from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import flourish_infant_admin

app_name = 'flourish_infant'

urlpatterns = [
    path('admin/', flourish_infant_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
]
