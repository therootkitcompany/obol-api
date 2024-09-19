from django.apps import AppConfig
from django.core.management import call_command

from django.db import connection

from shared.StripeUtils import create_stripe_clients


def load_initial_data():
    call_command('loaddata', 'organizations.json', verbosity=0)
    create_stripe_clients()


class OrganizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organization'

    def ready(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT to_regclass('organization_organization');")
                table_exists = cursor.fetchone()[0] is not None

            if table_exists:
                load_initial_data()
        except Exception as e:
            print(f"Error al cargar los datos iniciales: {e}")
