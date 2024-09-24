from decouple import config
from django.core.management import call_command

from shared.StripeUtils import create_stripe_clients


def deploy_and_migrate():
    if config("REMOTE_MIGRATE", default=False, cast=bool):
        call_command('migrate')
        return
    call_command('loaddata', 'organizations.json', verbosity=0)
    create_stripe_clients()
