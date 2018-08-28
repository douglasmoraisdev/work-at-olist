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

    STANDING_CHARGE = 0.36
    NORMAL_CALL_CHARGE = 0.09
    REDUCED_CALL_CHARGE = 0.0
    REDUCED_TIME_BEGIN = 22
    REDUCED_TIME_END = 6
    subscriber = models.CharField(max_length=11, blank=False, null=False)
    period = models.CharField(max_length=7, blank=False, null=False)

    def __str__(self):
        return self.subscriber+' - '+self.period

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
