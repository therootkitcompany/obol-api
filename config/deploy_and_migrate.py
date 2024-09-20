import os

import requests
from decouple import config


def deploy_and_migrate():
    deploy_hook_url = config('VERCEL_DEPLOY_HOOK_URL', default=None)
    migrate_command = "python manage.py migrate"
    if deploy_hook_url is None: return

    response = requests.post(deploy_hook_url)
    if response.status_code == 200:
        print("Despliegue exitoso.")

        os.system(migrate_command)
        print("Migraciones ejecutadas con éxito.")
    else:
        print(f"Error al desplegar: {response.content}")


if __name__ == "__main__":
    deploy_and_migrate()
