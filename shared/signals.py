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
        test(instance)


def test(donation):
    try:

        paymentIntent = stripe.PaymentIntent.retrieve(donation.stripePaymentId)
        receiptUrl = stripe.Charge.retrieve(paymentIntent.latest_charge).receipt_url
        save_charge(paymentIntent, receiptUrl, donation)
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


def save_charge(payment, receiptUrl, donation):
    saveCharge: Charge = Charge()
    saveCharge.status = payment.status
    saveCharge.receiptUrl = receiptUrl
    saveCharge.paymentMethod = payment.payment_method
    saveCharge.transferId = payment.id
    applicationFeeAmount = payment.application_fee_amount if payment.application_fee_amount is not None else 0
    saveCharge.amountReceived = payment.amount - applicationFeeAmount
    saveCharge.applicationFee = applicationFeeAmount
    saveCharge.currency = payment.currency
    saveCharge.description = payment.description
    saveCharge.donation = donation
    saveCharge.save()
