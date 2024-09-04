import uuid

import Adyen
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from config import settings
from donation.models import Donation

import stripe

stripe.api_key = settings.STRIPE_KEY


@receiver(post_save, sender=Donation)
def create_donation(sender, instance, created, **kwargs):
    if created:
        # do_transfer(instance.creditToken, instance.amount, instance.organization.bankAccount)
        testAdyen(instance.amount, instance.creditToken)


def testAdyen(amount, token):
    adyen = Adyen.Adyen()
    adyen.client.platform = "test"
    adyen.client.xapikey = settings.ADYEN_API_KEY

    payment_data = {
        'amount': {
            'value': amount,
            'currency': 'EUR'
        },
        'reference': generate_reference(),
        'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
        "paymentMethod": {
            "type": "scheme",
            "encryptedCardNumber": "test_5555555555554444",
            "encryptedExpiryMonth": "test_03",
            "encryptedExpiryYear": "test_2030",
            "encryptedSecurityCode": "test_737"
        },
        'metadata': {
            'type': 'donation',
            'cause': 'charity-name'
        }
    }

    # result = adyen.checkout.payments_api.payments(payment_data)
    json_request = {
        "amount": {
            "value": amount,
            "currency": "USD"
        },
        "card": {
            "number": "4111111111111111",
            "expiryMonth": "03",
            "expiryYear": "2030",
            "holderName": "John Smith"
        },
        "billingAddress": {
            "houseNumberOrName": "121",
            "street": "Brannan Street",
            "city": "Beverly Hills",
            "postalCode": "90210",
            "stateOrProvince": "CA",
            "country": "US"
        },
        "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
        "reference": generate_reference(),
        "shopperName": {
            "firstName": "John",
            "lastName": "Smith"
        },
        "nationality": "NL"
    }

    # Make the API call
    result = adyen.payout.instant_payouts_api.payout(request=json_request)

    return result


def generate_reference():
    return str(uuid.uuid4())


def do_transfer(creditToken, amount, bankAccount):
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency='eur',
            description='Donation test',
            source=creditToken,
        )

        transfer = stripe.Transfer.create(
            amount=int(amount * 0.8),
            currency="eur",
            destination='acct_1PJc2lBLXLGx5g20',
            description="Test",
        )
        return charge, transfer
    except stripe.error.CardError as e:
        print("Error al procesar la transacción:", str(e))
        return None


def get_destination():
    cliente = stripe.Customer.retrieve('cus_Q9VrNKcw6NpZO4')
    if 'default_source' in cliente:
        default_source = stripe.Source.retrieve('pm_1PJCpZIvP36SEYQg6tfvn00k')
        if default_source.object == 'source':
            if default_source.type == 'sepa_debit':
                return default_source.id
    return None
