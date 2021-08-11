from django.db import models
from django.utils.timezone import now
from users.models import User
# Create your models here.


class Loan(models.Model):
    SIX_MONTHS = 1
    ONE_YEAR = 2
    TWO_YEAR = 3

    DURATION_CHOICES = (
        (SIX_MONTHS, '6m'),
        (ONE_YEAR, '1y'),
        (TWO_YEAR, '2y')
    )

    PENDING = 1
    APPROVED = 2
    DENIED = 3

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DENIED, 'Denied')
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=10)
    started = models.DateTimeField(default=now())
    duration = models.CharField(
        max_length=2, choices=DURATION_CHOICES)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.amount
