from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Flourish Child'
    site_header = 'Flourish Child'
    index_title = 'Flourish Child'
    site_url = '/administration/'
    enable_nav_sidebar = False


flourish_child_admin = AdminSite(name='flourish_child_admin')
