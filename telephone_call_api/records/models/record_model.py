import uuid

from django.db import models
from rest_framework.exceptions import NotFound, ValidationError

from bills.models import Bill


class Record(models.Model):
    """Represent a Record data model

    Contains the fields and business logic of a Record entity.
    Each pair of successful registration calls (Start / End) generates
    a new bill record with your charge (a call price).

    Attributes:
        call_type(mandatory): Type of a record. Accepted
            values are START_CALL_TYPE or END_CALL_TYPE
        timestamp(mandatory): Date and Time the record occurs.
        call_id(mandatory): Identifier a record pair (Start/End).
        source(mandatory): The phone number of the caller.
        destination(mandatory): The phone number of the recipient.
        bill(optional): The Bill that the record belong
    """

    START_CALL_TYPE = 'S'
    END_CALL_TYPE = 'E'
    TYPE_CALL_CHOICES = (
        (START_CALL_TYPE, 'Start'),
        (END_CALL_TYPE, 'End')
    )

    call_type = models.CharField(max_length=1, blank=False, 
                                 null=False, choices=TYPE_CALL_CHOICES)
    timestamp = models.DateTimeField(blank=False, null=False)
    call_id = models.IntegerField(blank=False, unique=False, null=False)
    source = models.CharField(max_length=11, blank=False, null=False)
    destination = models.CharField(max_length=11, blank=False, null=False)
    bill = models.ForeignKey('bills.Bill', on_delete=models.CASCADE,
                             blank=True, null=True, unique=False)

    def __str__(self):
        return self.source+' - '+self.call_type+' - '+str(self.call_id)
