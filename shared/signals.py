from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from charges.models import Charge
from config import settings
from donation.models import Donation

import stripe

from shared.errorHandler import StripeChargeError

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
            ip=donation.clientIp,
            metadata={
                'donor_email': donation.email,
                'donor_name': donation.name + donation.surname,
                'donation_purpose': 'Church Fundraiser',
                'connected_account_name': donation.organization.name,
                'connected_account_email': donation.organization.email,
                'event_date': now()
            }
        )
        donation.creditToken = settings.cipher_suite.encrypt(donation.creditToken.encode())
        donation.save()
        save_charge(charge, donation)
    except stripe.error.CardError as e:
        body = e.json_body
        err = body.get('error', {})
        raise_error(f"Your card was declined: {err.get('message')}", 402, donation)
    except stripe.error.RateLimitError as e:
        raise_error("Rate limit exceeded, please try again later.", 429, donation)
    except stripe.error.InvalidRequestError as e:
        raise_error(f"Invalid request: {e}", 400, donation)
    except stripe.error.AuthenticationError as e:
        raise_error("Authentication failed, please check your API keys.", 401, donation)
    except stripe.error.APIConnectionError as e:
        raise_error("Network communication with Stripe failed.", 503, donation)
    except stripe.error.StripeError as e:
        raise_error("An error occurred with Stripe, please try again later.", 500, donation)
    except Exception as e:
        raise_error(f"An unexpected error occurred: {e}", 500, donation)


def raise_error(message, code, donation):
    donation.delete()
    raise StripeChargeError(message, code)


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
