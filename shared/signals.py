from django.db.models.signals import post_save
from django.dispatch import receiver

from config import settings
from donation.models import Donation

import stripe

stripe.api_key = settings.STRIPE_KEY;


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
