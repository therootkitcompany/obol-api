from decouple import config
from django.core.management import call_command

from shared.StripeUtils import create_stripe_clients


def deploy_and_migrate():
    if config("REMOTE_MIGRATE", default=False, cast=bool):
        call_command('migrate')
        return
    try:
        call_command('loaddata', 'projects.json', verbosity=0)
        call_command('loaddata', 'organizations.json', verbosity=0)
    except Exception as e:
        print("Error loading fixture:", e)
