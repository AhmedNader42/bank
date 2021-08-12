from django.db import models

class Bank(models.Model):
    total_amount = models.DecimalField(max_digits=19, decimal_places=5)

