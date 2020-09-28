from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Flourish Infant'
    site_header = 'Flourish Infant'
    index_title = 'Flourish Infant'
    site_url = '/administration/'
    enable_nav_sidebar = False


flourish_infant_admin = AdminSite(name='flourish_infant_admin')
