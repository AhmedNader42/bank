from django.db import models
from django.utils.timezone import now
from users.models import User
# Create your models here.


class LoanOption(models.Model):
    id = models.BigAutoField(primary_key=True)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=3)
    maximum_amount = models.DecimalField(max_digits=19, decimal_places=5)
    duration = models.PositiveIntegerField()
    interest_rate = models.PositiveIntegerField()


class Loan(models.Model):
    PENDING = 1
    APPROVED = 2
    DENIED = 3

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DENIED, 'Denied')
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.ForeignKey(LoanOption, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=19, decimal_places=5)
    started = models.DateTimeField(default=now())

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.amount
