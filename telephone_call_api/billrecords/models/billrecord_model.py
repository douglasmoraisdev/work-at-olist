import uuid

from django.db import models
from django.db.models import Count

class BillRecord(models.Model):
    """Represent a Bill Record data model

    Contains the fields and business logic of a Bill Record entities.
    This model represents the charge record of a call.
    
    Attributes:
        bill_origin (mandatory): The origin Bill of the bill record.
        start_call (mandatory): The origin start call (Start Type).
        end_call (mandatory): The origin end call (End Type).
        call_price (mandatory): The call charge.
    """

    bill_origin = models.ForeignKey('bills.Bill', on_delete=models.CASCADE,
                                    blank=True, null=True, unique=False)
    start_call = models.ForeignKey('records.Record', on_delete=models.CASCADE,
                                   related_name='start_call', blank=True,
                                   null=True, unique=False)
    end_call = models.ForeignKey('records.Record', on_delete=models.CASCADE,
                                 related_name='end_call', blank=True,
                                 null=True, unique=False)
    call_price = models.FloatField()
