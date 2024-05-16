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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if not re.match(r'^[0-9]{9,18}$', self.bankAccount):
            raise ValidationError("The bank account number must contain between 9 and 18 numeric digits.")

    def mask_bankAccount(self):
        return self.bankAccount[:4] + '*' * (len(self.bankAccount) - 8) + self.bankAccount[-4:]

    class Meta:
        ordering = ['-id']
