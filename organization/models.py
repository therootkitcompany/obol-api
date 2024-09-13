from email.policy import default

from django.utils import timezone

from django.core.validators import EmailValidator, MaxLengthValidator, RegexValidator
from django.db import models
import re
from django.core.exceptions import ValidationError


class Organization(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    description = models.CharField(max_length=10000, null=False)
    email = models.EmailField(
        validators=[
            EmailValidator(message="Please enter a valid email address."),
            MaxLengthValidator(254, message="Email address must be at most 254 characters long.")
        ],
        null=False,
        blank=False
    )
    phoneRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be in the correct format.")
    phone = models.CharField(max_length=17, validators=[phoneRegex], blank=True)
    bankAccount = models.CharField(max_length=50)
    countryCodeRegex = RegexValidator(regex=r'^[A-Z]{2}$',
                                      message="Enter the country code (ISO 3166-1 alpha-2), e.g., 'US' for the United States")
    countryCode = models.CharField(max_length=2,
                                   validators=[countryCodeRegex],
                                   default="VA"
                                   )
    currencyRegex = RegexValidator(regex=r'^[A-Z]{3}$',
                                   message="Enter the currency code (ISO 4217), e.g., 'USD' for U.S. dollars or 'EUR' for euros")
    currency = models.CharField(max_length=2,
                                validators=[currencyRegex],
                                default="EUR"
                                )
    line1 = models.CharField(max_length=1000, default="Via Della Conciliazione")
    city = models.CharField(max_length=50, default="City of Vatican")
    state = models.CharField(max_length=50, default="Vatican")
    postalCode = models.CharField(max_length=50, default="00120")
    web = models.CharField(max_length=100, default="https://www.vatican.va/")
    stripeId = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        super().clean()
        if not re.match(r'^[0-9]{9,18}$', self.bankAccount):
            raise ValidationError("The bank account number must contain between 9 and 18 numeric digits.")

    # def mask_bankAccount(self):
    #     return self.bankAccount[:4] + '*' * (len(self.bankAccount) - 8) + self.bankAccount[-4:]

    class Meta:
        ordering = ['-id']
