import time

import stripe

from config import settings

stripe.api_key = settings.STRIPE_KEY


def create_stripe_clients():
    from organization.models import Organization
    organizations = Organization.objects.all()
    for organization in organizations:
        create_stripe_client(organization)


def create_stripe_client(organization):
    client = get_client_by_email(organization.email)
    if client is None:
        newClient = stripe.Customer.create(
            name=organization.name,
            email=organization.email,
            phone=organization.phone,
        )
        add_bank_account(newClient, organization.bankAccount)


def get_client_by_email(email):
    clients = stripe.Customer.list(email=email, limit=1)
    if clients.data:
        return clients.data[0]
    return None


def add_bank_account(client, account_number):
    payment_method = stripe.PaymentMethod.create(
        type="sepa_debit",
        sepa_debit={
            "iban": account_number,
        },
        billing_details={
            "name": client.name,
            "email": client.email
        }
    )
    stripe.PaymentMethod.attach(
        payment_method.id,
        customer=client.id
    )
    stripe.Customer.modify(
        client.id,
        invoice_settings={"default_payment_method": payment_method.id}
    )
