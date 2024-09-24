import uuid

from django.core.validators import EmailValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.db.models.deletion import CASCADE

from organization.models import Organization


# Create your models here.

class Donation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        validators=[
            EmailValidator(message="Please enter a valid email address."),
            MaxLengthValidator(254, message="Email address must be at most 254 characters long.")
        ],
        null=False,
        max_length=50,
        blank=False
    )
    name = models.CharField(max_length=255, null=False)
    surname = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.PositiveIntegerField(default=1)
    currencyRegex = RegexValidator(regex=r'^[A-Z]{3}$',
                                   message="Enter the currency code (ISO 4217), e.g., 'USD' for U.S. dollars or 'EUR' for euros")
    currency = models.CharField(max_length=3,
                                validators=[currencyRegex],
                                default="EUR"
                                )
    country = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100, message="Country name must be at most 100 characters long.")
        ],
        null=False,
        blank=False
    )
    city = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100, message="City name must be at most 100 characters long.")
        ],
        null=False,
        blank=False
    )
    stripePaymentId = models.CharField(max_length=255, unique=True, null=False, blank=False, default='Anonymous')
    clientIp = models.GenericIPAddressField(protocol='both', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=CASCADE, related_name="donations",
                                     related_query_name='donation',
                                     null=False, blank=False)

    class Meta:
        ordering = ['-id']
