from django.core.validators import EmailValidator, MaxLengthValidator
from django.db import models


# Create your models here.

class Donation(models.Model):
    email = models.EmailField(
        validators=[
            EmailValidator(message="Please enter a valid email address."),
            MaxLengthValidator(254, message="Email address must be at most 254 characters long.")
        ],
        null=False,
        blank=False
    )
    name = models.CharField(max_length=255, null=False)
    surname = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=255, default="Pending")
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

    class Meta:
        ordering = ['-id']
