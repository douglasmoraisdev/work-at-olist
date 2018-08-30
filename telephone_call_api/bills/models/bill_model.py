import uuid
import datetime
from datetime import timedelta

from django.db import models
from django.db.models import Count

from billrecords.models import BillRecord


class Bill(models.Model):
    """Represent a Bill data model

    Contains the fields and business logic of a Bill entities.
    Calculates the call prices and generate bill records.

    Attributes:
        subscriber (mandatory): The subscriber of Bill (caller).
        period (mandatory): The reference period of Bill (month/year).
            format string = (mm/yyyy).
    """

    STANDING_CHARGE = 0.36
    NORMAL_CALL_CHARGE = 0.09
    REDUCED_CALL_CHARGE = 0.0
    REDUCED_TIME_BEGIN = 22
    REDUCED_TIME_END = 6
    subscriber = models.CharField(max_length=11, blank=False, null=False,
                                  help_text="Subscriber phone number"
                                  )
    period = models.CharField(max_length=7, blank=False, null=False,
                              help_text="The Period of a Bill. Format (MMYYYY)"
                              )

    def __str__(self):
        return self.subscriber+' - '+self.period

    def update_bill_record(self, start_call, end_call):
        """Create a new call change record

        Send Start call and End call data to generate
        a new call change record on database
        """

        # Receive Start and End call from parameters
        _start_period = start_call.timestamp
        _end_period = end_call.timestamp

        # Create a new BillRecord object
        _bill_record = BillRecord()

        # Populate the object and save
        _bill_record.bill_origin = end_call.bill
        _bill_record.start_call = start_call
        _bill_record.end_call = end_call
        _bill_record.call_price = self.calculate_charge(
                                    _start_period, _end_period
                                  )
        _bill_record.save()

    def calculate_charge(self, start_period, end_period):
        """Calculate a call charge

        Calculation Formula:
            Call Charge =
                Base charge
                +(
                    (call minute * Normal charge)
                    + (call minute * Reduced charge)
                )

            Base charge (cost of a connection): STANDING_CHARGE
            Normal charge (calls Between 6h and 22h): NORMAL_CALL_CHARGE
            Reduced charge (calls Between 22h and 6h): REDUCED_CALL_CHARGE
            For REDUCED_TIME_BEGIN = 22h and REDUCED_TIME_END = 6h

            Example:
            For a call started at 21:57:13 and finished at 22:10:56 we have:
                Standing charge: R$ 0,36
                Normal charge: R$ 0,09
                Reduced charge: R$ 0,00
                Call charge:
                    Minutes in normal time between 21:57:13 and 22:00 = 2
                    Price: 2 * R$ 0,09 = R$ 0,18
                Total = R$ 0,36 + R$ 0,18 = 0,54
        """

        # Convert time charges on timedelta for simplify calculation
        _start_reduced_time = timedelta(hours=self.REDUCED_TIME_BEGIN)
        _end_reduced_time = timedelta(hours=self.REDUCED_TIME_END)

        # Initialize variables for the time comparision loop
        _normal_charge_minutes = 0
        _reduced_charge_minutes = 0
        _period_comparison = start_period + timedelta(minutes=1)

        # Contabilize the minutes in normal time and/or reduced time
        while (_period_comparison <= end_period):

            _period_delta = timedelta(hours=_period_comparison.hour,
                                      minutes=_period_comparison.minute,
                                      seconds=_period_comparison.second)

            # Verify the contabilized minute is in normal time or reduced time
            if (_period_delta < _start_reduced_time) and \
               (_period_delta >= _end_reduced_time+timedelta(minutes=1)):
                _normal_charge_minutes += 1
            else:
                _reduced_charge_minutes += 1

            # Go to next minute
            _period_comparison += timedelta(minutes=1)

        # Calculate the minutes charge
        _total_charge = round(_normal_charge_minutes
                              * self.NORMAL_CALL_CHARGE
                              + _reduced_charge_minutes
                              * self.REDUCED_CALL_CHARGE
                              + self.STANDING_CHARGE,
                              2)

        return _total_charge

    def get_last_closed_period(self, actual_period=None):
        """Return the last month period string in MMYYYY format

        Attributes:
            actual_period(optional): The actual date of the query
        """

        if actual_period is None:
            actual_period = datetime.datetime.now()

        # Verify January case (subtract one year)
        if actual_period.month > 1:
            _last_month = actual_period.month - 1
            _year_period = actual_period.year
        else:
            _year_period = actual_period.year - 1
            _last_month = 12

        # Format mount string
        if _last_month < 10:
            _last_month_str = '0%d' % _last_month
        else:
            _last_month_str = _last_month

        # Format the final result
        _last_period = '%s%s' % (_last_month_str, _year_period)

        return _last_period
