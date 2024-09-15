from django.db.models.signals import post_save
from django.dispatch import receiver

from config import settings
from donation.models import Donation

import stripe

stripe.api_key = settings.STRIPE_KEY


@receiver(post_save, sender=Donation)
def create_donation(sender, instance, created, **kwargs):
    if created:
        do_transfer(instance.creditToken, instance.amount, instance.organization)


def do_transfer(creditToken, amount, account):
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=account.currency,
            description='Donation test',
            source=creditToken,
            transfer_data={
                'destination': account.stripeId,
            },
            application_fee_amount=int(amount * 0.25),
        )
        return charge
    except stripe.error.CardError as e:
        print("Error al procesar la transacción:", str(e))
        return None
