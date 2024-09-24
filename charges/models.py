import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.db.models.deletion import CASCADE

from donation.models import Donation


class Charge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20)
    receiptUrl = models.URLField(blank=True, null=True)
    paymentMethod = models.CharField(max_length=255, blank=True, null=True)
    transferId = models.CharField(max_length=255, blank=True, null=True)
    amountReceived = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    applicationFee = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    currencyRegex = RegexValidator(regex=r'^[A-Z]{3}$',
                                   message="Enter the currency code (ISO 4217), e.g., 'USD' for U.S. dollars or 'EUR' for euros")
    currency = models.CharField(max_length=3,
                                validators=[currencyRegex],
                                default="EUR"
                                )
    description = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    donation = models.ForeignKey(Donation, on_delete=CASCADE, related_name="charges",
                                 related_query_name='charge',
                                 null=False, blank=False)

    class Meta:
        ordering = ['-id']
