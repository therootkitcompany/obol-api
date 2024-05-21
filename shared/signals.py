from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from config import settings
from donation.models import Donation

import stripe

from organization.models import Organization
from shared.StripeUtils import create_stripe_client

stripe.api_key = settings.STRIPE_KEY


@receiver(post_migrate)
def create_stripe_clients(sender, **kwargs):
    organizations = Organization.objects.all()
    for organization in organizations:
        create_stripe_client(organization)


@receiver(post_save, sender=Donation)
def do_transfer(sender, instance, created, **kwargs):
    if created:
        test(instance.creditToken, instance.amount, instance.organization.bankAccount)


def test(creditToken, amount, bankAccount):
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency='eur',
            description='Donation test',
            source=creditToken,
        )

        return charge
    except stripe.error.CardError as e:
        print("Error al procesar la transacción:", str(e))
        return None
