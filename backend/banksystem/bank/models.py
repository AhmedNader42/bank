from django.db import models


class Bank(models.Model):
    total_amount = models.DecimalField(max_digits=19, decimal_places=5)

    """
        In_flow is the amount of money coming into the bank.
        Whether it be right now or at some point in the future. 
        It works as a total of what the bank is getting in terms of money.
    """
    in_flow = models.DecimalField(max_digits=15, decimal_places=5, default=0.0)

    """
        out_flow is the amount of money the bank owes to it's funders.
        Whether it be right now or at some point in the future. 
        It works as a total of what the bank is paying the funders.
    """
    out_flow = models.DecimalField(
        max_digits=15, decimal_places=5, default=0.0)
