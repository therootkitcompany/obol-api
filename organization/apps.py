from django.apps import AppConfig
from django.core.management import call_command


class OrganizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organization'

    def ready(self):
        call_command('loaddata', 'organizations.json', verbosity=0)
