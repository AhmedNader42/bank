from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'banker'),
        (2, 'customer'),
        (3, 'funder')
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=2)


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)


# class Loan(models.Model):
