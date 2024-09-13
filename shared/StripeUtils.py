import stripe

from config import settings

stripe.api_key = settings.STRIPE_KEY


def create_stripe_clients():
    from organization.models import Organization
    organizations = Organization.objects.all()
    clients = stripe.Account.list(limit=1000)
    for organization in organizations:
        create_stripe_client(organization, clients)


def create_stripe_client(organization, clients):
    client = get_client_by_email(organization.email, clients)
    if client is None:
        bankAccount = create_bank_account(organization)
        client = create_account(organization, bankAccount)
    saveOrganization(organization, client.id)


def get_client_by_email(email, clients):
    for account in clients.data:
        if account.get('email') == email:
            return account
    return None


def create_bank_account(organization):
    return stripe.Token.create(
        bank_account={
            "country": organization.countryCode,
            "currency": organization.currency,
            "account_holder_name": organization.name + organization.description,
            "account_holder_type": "individual",
            "account_number": organization.bankAccount
        }
    )


def create_account(organization, bankAccount):
    account = stripe.Account.create(
        type="custom",
        country=organization.countryCode,
        email=organization.email,
        capabilities={
            'transfers': {'requested': True},
        },
        business_type="individual",
        individual={
            "first_name": organization.name,
            "last_name": organization.description,
            "email": organization.email,
            "address": {
                "line1": organization.line1,
                "city": organization.city,
                "state": organization.state,
                "postal_code": organization.postalCode,
                "country": organization.countryCode
            },
            "dob": {
                "day": 1,
                "month": 1,
                "year": 1980
            },
            "phone": organization.phone
        },
        external_account=bankAccount['id'],
        business_profile={
            "url": organization.web,
            "product_description": "Donation platform for " + organization.name
        }
    )

    stripe.Account.modify(
        account.id,
        tos_acceptance={"date": 1609798905, "ip": "8.8.8.8"},
    )

    return account


def saveOrganization(organization, accountId):
    organization.stripeId = accountId
    organization.save()
