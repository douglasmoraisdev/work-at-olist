import uuid
from datetime import timedelta

from django.db import models
from django.db.models import Count


class Bill(models.Model):
    """Represent a Bill data model

    Contains the fields and business logic of a Bill entities.
    Calculates the call prices and generate bill records.

    Attributes:
        subscriber (mandatory): The subscriber of Bill (caller).
        period (mandatory): The reference period of Bill (month/year).
            format string = (mm/yyyy).
    """

    subscriber = models.CharField(max_length=11, blank=False, null=False)
    period = models.CharField(max_length=7, blank=False, null=False)

    def __str__(self):
        return self.subscriber+' - '+self.period
