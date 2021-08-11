from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    BANKER = 1
    CUSTOMER = 2
    FUNDER = 3
    USER_TYPE_CHOICES = (
        (BANKER, 'banker'),
        (CUSTOMER, 'customer'),
        (FUNDER, 'funder')
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=2)
