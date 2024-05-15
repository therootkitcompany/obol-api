from django.core.validators import EmailValidator, MaxLengthValidator, RegexValidator
from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
