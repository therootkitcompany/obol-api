from django.apps import AppConfig

from config.deploy_and_migrate import deploy_and_migrate


class SharedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shared'

    def ready(self):
        from .signals import create_donation
        deploy_and_migrate()
