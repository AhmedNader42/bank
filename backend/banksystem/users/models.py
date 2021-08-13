from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    BANKER = 1
    CUSTOMER = 2
    FUNDER = 3
    USER_TYPE_CHOICES = (
        (BANKER, "Banker"),
        (CUSTOMER, "CUSTOMER"),
        (FUNDER, "FUNDER"),
    )

    user_type = models.PositiveSmallIntegerField(default=2)
