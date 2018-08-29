import uuid

from django.db import models
from rest_framework.exceptions import NotFound, ValidationError

from bills.models import Bill
from billrecords.models import BillRecord


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

    def save(self, *args, **kwargs):
        """Business rule for save a new Start or End call record

        Override the Record Save Method for implement business rule
        Verify Call Record consistency:
            - Only valid Call Record types are allowed:
                (START_CALL_TYPE or END_CALL_TYPE)
            - Only unique call_id per call type is allowed
            - A E type Call record only may exist if a origin S type
                Call record (same call_id) already exists
            - The end call date/time MAY be higher than
                the start call date/time
        """

        # Verify Call Type
        _valid_type = False
        for choise in self.TYPE_CALL_CHOICES:
            if self.call_type == choise[0]:
                _valid_type = True

        if not _valid_type:
            raise ValidationError({'detail': 'Invalid call record Type'})

        # Verify a call with same type and call_id already created
        if Record.objects.filter(call_id=self.call_id,
                                 call_type=self.call_type).exists():
            raise ValidationError(
                {'detail': 'This record call_id is already created'})

        # If a End Call record, generate a charge
        if self.call_type == self.END_CALL_TYPE:

            # Get the origin Start Call
            _origin_start_call = Record.objects.filter(
                call_id=self.call_id, call_type=self.START_CALL_TYPE)

            if not _origin_start_call.exists():
                raise NotFound('Origin start call record not Found')

            # Verify the Start and End date/time consistency
            if _origin_start_call.get().timestamp > self.timestamp:
                raise ValidationError(
                                      {'detail': 'Date/time from origin \
                                      start call is higher then end call'})

            # Get the period string
            # The end call date determine his bill period
            _end_call_period = self.timestamp.strftime("%m%Y")

            self.source = _origin_start_call.get().source
            self.destination = _origin_start_call.get().destination

            # Get a already created bill for the period
            _already_created_bill = Bill.objects.filter(
                                                        period=_end_call_period
                                                        )
            if _already_created_bill.exists():
                self.bill = _already_created_bill.get()

            # If not found a already created Bill, create a new one
            else:
                _new_created_bill = Bill()
                _new_created_bill.subscriber = self.source
                _new_created_bill.period = _end_call_period
                _new_created_bill.save(self)

                self.bill = _new_created_bill

            # save the information of bill on the origin
            # start call record
            _origin_start_call.update(bill=self.bill)

            # save the current end call record
            super(Record, self).save(*args, **kwargs)

            # update the bill
            Bill().update_bill_record(_origin_start_call.get(), self)

        else:
            # Verify a start call with same source and destination number
            if (self.source == self.destination):
                raise ValidationError(
                        {'detail': 'Same source and destination numbers'})

            super(Record, self).save(*args, **kwargs)
