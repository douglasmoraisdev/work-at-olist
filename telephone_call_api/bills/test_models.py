import time
import datetime
from datetime import timedelta

from django.test import TestCase

from bills.models import Bill
from billrecords.models import BillRecord
from records.models import Record


class CalculateCallTaxTestCase(TestCase):
    """Test Bill calculate charge bussiness rule"""

    def setUp(self):
        pass

    def test_normal_time_call_charge(self):
        """
        Test a 10 mins normal time call
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 15:07:10", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 15:17:40", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 1.26)

    def test_normal_time_call_charge_minus_1sec(self):
        """
        Test a 9mins 59sec call in normal time
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 15:07:10", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 15:17:09", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 1.17)

    def test_o_clock_to_reduced_22h_charge(self):
        """
        Test a 1hour 00sec call ended at begin reduced time o'clock
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 21:00:00", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 22:00:00", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 1.17)

    def test_o_clock_to_reduced_22h_charge(self):
        """
        Test a 10 mins call ended at the begin of a reduced time o'clock
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 21:50:00", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 22:00:00", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 1.17)

    def test_o_clock_to_reduced_22h_plus_1sec_charge(self):
        """
        Test a 10 mins call ended at the begin of a reduced time plus 1sec
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 21:50:00", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 22:00:01", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 1.17)

    def test_o_clock_to_reduced_6h_charge(self):
        """
        Test a 10 mins call ended at the end of a reduced time o'clock
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 05:50:00", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 06:00:00", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 0.36)

    def test_o_clock_to_reduced_6h_plus_1sec_charge(self):
        """
        Test a 10 mins call ended at the end of a reduced time
            plus 1 sec
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 05:50:00", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 06:00:01", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 0.36)

    def test_o_clock_6h_plus_1min_charge(self):
        """
        Test a 1 min call ended at the end of a reduced call plus 1 min
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 06:00:00", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 06:01:00", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 0.45)

    def test_6h1s_plus_1min_charge(self):
        """
        Test a 59secs call started at 1 second after a end reduced time
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 06:00:01", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 06:01:00", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 0.36)

    def test_half_hour_to_reduced_charge(self):
        """
        Test a 40mins call started at 30mins before a reduced time
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 21:30:10", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 23:10:10", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 2.97)

    def test_2_mins_to_reduced_charge(self):
        """
        Test a 13 mins call started at 3 mins before a reduced time
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 21:57:13", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 23:10:56", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 0.54)

    def test_cross_from_reduced_to_charge(self):
        """
        Test a call started on a reduced time and ended at normal time
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-25 23:25:10", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 10:15:10", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 23.31)

    def test_24h_call_charge(self):
        """
        Test a 24 hours call
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 14:58:08", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-27 14:58:08", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 86.67)

    def test_48h_call_charge(self):
        """
        Test a 48 hours call
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 14:58:08", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-28 14:58:08", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 172.98)

    def test_reduced_time_call_charge(self):
        """
        Test a call that started and ended into a reduced time
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 22:00:00", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-27 06:00:00", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 0.36)

    def test_max_normal_time_call_in_a_day_charge(self):
        """
        Test a call that started and ended into a normal time
        """
        ts_begin = datetime.datetime.strptime(
            "2018-08-26 06:00:00", "%Y-%m-%d %H:%M:%S")
        ts_end = datetime.datetime.strptime(
            "2018-08-26 22:00:00", "%Y-%m-%d %H:%M:%S")

        _one_minute_call_price = Bill().calculate_charge(ts_begin, ts_end)

        self.assertEqual(_one_minute_call_price, 86.67)


class UpdateBillRecordTestCase(TestCase):
    """Test Bill update bussiness rule"""

    def setUp(self):
        pass

    def test_bill_update(self):
        """
        Test a Bill update (new Bill record)
        """

        _start_call = Record()
        _start_call.timestamp = datetime.datetime.strptime(
                                  "2018-08-26T15:07:10+0000",
                                  "%Y-%m-%dT%H:%M:%S%z")
        _start_call.source = '51992657100'
        _start_call.destination = '5133877079'
        _start_call.call_type = 'S'
        _start_call.call_id = '1'
        _start_call.save()

        _end_call = Record()
        _end_call.timestamp = datetime.datetime.strptime(
                                  "2018-08-26T15:17:10+0000",
                                  "%Y-%m-%dT%H:%M:%S%z")
        _end_call.call_type = 'E'
        _end_call.call_id = '1'
        _end_call.save()

        _start_period = _start_call.timestamp
        _end_period = _end_call.timestamp

        _bill = Bill()
        _bill.subscriber = '51992657100'
        _bill.period = '072018'
        _bill.save()

        _bill_record = BillRecord()
        _bill_record.bill_origin = _bill
        _bill_record.start_call = _start_call
        _bill_record.end_call = _end_call
        _bill_record.call_price = _bill.calculate_charge(
                                    _start_period, _end_period
                                  )
        _bill_record.save()

        self.assertEquals(BillRecord.objects.filter(
                                            bill_origin=_bill).count(), 1)


class LastBillRulePeriodTestCase(TestCase):

    def setUp(self):
        pass

    def test_last_period_in_jan_2018(self):
        """Test a cross year last month (January to December)"""

        _jan_18_date = datetime.datetime.strptime("2018-01-01T", "%Y-%m-%dT")

        _last_period = Bill().get_last_closed_period(_jan_18_date)

        self.assertEquals(_last_period, '122017')

    def test_last_period_in_feb_2018(self):
        """Test rule on February month"""

        _feb_18_date = datetime.datetime.strptime("2018-02-01T", "%Y-%m-%dT")

        _last_period = Bill().get_last_closed_period(_feb_18_date)

        self.assertEquals(_last_period, '012018')

    def test_last_period_in_mar_2018(self):
        """Test rule on March month"""

        _mar_18_date = datetime.datetime.strptime("2018-03-01T", "%Y-%m-%dT")

        _last_period = Bill().get_last_closed_period(_mar_18_date)

        self.assertEquals(_last_period, '022018')

    def test_last_period_in_dec_2018(self):
        """Test rule on December month"""

        _dec_18_date = datetime.datetime.strptime("2018-12-01T", "%Y-%m-%dT")

        _last_period = Bill().get_last_closed_period(_dec_18_date)

        self.assertEquals(_last_period, '112018')
