import stripe

from config import settings
from organization.models import Organization

stripe.api_key = settings.STRIPE_KEY


def create_stripe_client(organization: Organization):
    client = get_client_by_email(organization.email)
    if client is None:
        newClient = stripe.Customer.create(
            name=organization.name,
            email=organization.email,
            phone=organization.phone
        )
        print(f"Cliente creado: {newClient.id}")


def get_client_by_email(email):
    clients = stripe.Customer.list(email=email, limit=1)
    if clients.data:
        return clients.data[0]
    return None
