from decouple import config
from django.core.management import call_command


def deploy_and_migrate():
    if config("REMOTE_MIGRATE", default=False, cast=bool): return
    call_command('migrate')
    print('Data migrate')
