import uuid

from django.db import models
from rest_framework.exceptions import NotFound, ValidationError

class Record(models.Model):
    """Represent a Record data model

    Contains the fields and business logic of a Record entities.
    
    Attributes:
        call_type (char, max length = 1): Type of a record. Accepted
            values are START_CALL_TYPE or END_CALL_TYPE
        timestamp: Date and Time the record occurs.
        call_id: Identifier a record pair (Start/End).
        source: The phone number of the caller
        destination: The phone number of the recipient
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

    def __str__(self):
        return self.source+' - '+self.call_type+' - '+str(self.call_id)
