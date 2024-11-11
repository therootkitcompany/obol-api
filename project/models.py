import uuid

from django.db import models
from django.db.models import Sum
from django.utils import timezone


# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    goal = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('in-progress', 'In progress'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    totalAmount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    totalDonations = models.IntegerField(default=0)
    commission = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    endDate = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    @property
    def totalAmount(self):
        from donation.models import Donation
        return Donation.objects.filter(organization__project=self).aggregate(total=Sum('amount'))['total'] or 0

    @property
    def totalDonations(self):
        from donation.models import Donation
        return Donation.objects.filter(organization__project=self).count()

    @property
    def progress(self):
        if self.goal and self.goal > 0:
            return min((self.totalAmount / self.goal) * 100, 100)
        return 0
