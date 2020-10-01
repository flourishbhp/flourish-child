from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'flourish_child'
    verbose_name = 'Flourish Child'
    admin_site_name = 'flourish_child_admin'
