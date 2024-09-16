from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from charges.models import Charge
from config import settings
from donation.models import Donation

import stripe

stripe.api_key = settings.STRIPE_KEY


@receiver(post_save, sender=Donation)
def create_donation(sender, instance, created, **kwargs):
    if created:
        do_transfer(instance)


def do_transfer(donation):
    try:
        charge = stripe.Charge.create(
            amount=donation.amount,
            currency=donation.currency,
            description='Donation test',
            source=donation.creditToken,
            receipt_email=donation.email,
            on_behalf_of=donation.organization.stripeId,
            transfer_data={
                'destination': donation.organization.stripeId,
            },
            application_fee_amount=int(donation.amount * 0.25),
            metadata={
                'donor_email': donation.email,
                'donor_name': donation.name + donation.surname,
                'donation_purpose': 'Church Fundraiser',
                'connected_account_name': donation.organization.name,
                'connected_account_email': donation.organization.email,
                'event_date': now()
            }
        )
        save_charge(charge, donation)
    except stripe.error.CardError as e:
        print("Error al procesar la transacción:", str(e))
        return None


def save_charge(charge, donation):
    saveCharge: Charge = Charge()
    saveCharge.status = charge.status
    saveCharge.receiptUrl = charge.receipt_url
    saveCharge.paymentMethod = charge.payment_method
    saveCharge.transferId = charge.transfer
    saveCharge.amountReceived = charge.amount_captured - charge.application_fee_amount
    saveCharge.applicationFee = charge.application_fee_amount
    saveCharge.currency = charge.currency
    saveCharge.donation = donation
    saveCharge.save()
