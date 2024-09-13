from django.utils import timezone
from django.apps import AppConfig
from django.core.management import call_command

from shared.StripeUtils import create_stripe_clients


def load_initial_data():
    call_command('loaddata', 'organizations.json', verbosity=0)
    create_stripe_clients()


class OrganizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organization'

    def ready(self):
        load_initial_data()
