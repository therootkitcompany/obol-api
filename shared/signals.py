from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from config import settings
from donation.models import Donation

import stripe

stripe.api_key = settings.STRIPE_KEY


@receiver(post_save, sender=Donation)
def create_donation(sender, instance, created, **kwargs):
    if created:
        do_transfer(instance.creditToken, instance.amount, instance.organization.bankAccount)


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
