from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'flourish_infant'
    verbose_name = 'Flourish Infant'
    admin_site_name = 'flourish_infant_admin'
