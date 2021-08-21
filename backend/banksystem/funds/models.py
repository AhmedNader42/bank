from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.


class FundOption(models.Model):
    id = models.BigAutoField(primary_key=True)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=3)
    maximum_amount = models.DecimalField(max_digits=19, decimal_places=5)
    duration = models.PositiveIntegerField()
    interest_rate = models.PositiveIntegerField()


class Fund(models.Model):
    PENDING = 1
    APPROVED = 2
    DENIED = 3

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DENIED, 'Denied')
    )

    funder = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(FundOption, on_delete=models.CASCADE)
    payment_url = models.CharField(max_length=500, default="")

    amount = models.DecimalField(max_digits=19, decimal_places=5)
    started = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES)
    payment_verified = models.BooleanField(default=False)
    payment_receipt_url = models.CharField(max_length=500, default="")

    def __str__(self):
        return str(self.amount)
