import unittest
import sys
import datetime
import check_data_sheet
from unittest.mock import patch


class TestCheckDataSheet(unittest.TestCase):

    test_header_keys = ['TimeZone', 'Localtime', 'localms', 'UTC ', 'DID', 'RH1', 'W', 'L1', 'L2', 'T1', 'T2', 'RH2', 'B1', 'B2', 'V', 'BB1', 'BB2', 'F']

    def test_last_row(self):
        test_args = ["check_data_sheet.py"]
        with patch.object(sys, 'argv', test_args):
            result = check_data_sheet.main()
            self.assertIsNotNone(result, "Sheet's last row is None!")
            self.assertIsInstance(result, dict, "Result data is not an instance of the dict")
            self.assertTrue(all([i.strip() in result for i in self.test_header_keys]), "Incorrect dict structure")
            self.assertTrue(any([i is not None for i in result.values()]), "Incorrect dict structure")

    def test_timestamp_convert(self):
        test_ts = 1558405365495
        test_result = datetime.datetime(2019, 5, 21, 2, 22, 45)
        result = check_data_sheet.utc_time_stamp_to_utc_datetime(test_ts)
        self.assertEqual(test_result, result, "UTC converter datetime objects are not equal")

    def test_localtime_convert(self):
        test_timezone = "America/Los_Angeles"
        test_local_time = "5/20/2019 19:22:45"
        test_result = datetime.datetime(2019, 5, 21, 2, 22, 45)
        result = check_data_sheet.local_time_zone_to_utc_datetime(test_local_time, test_timezone)
        self.assertEqual(test_result, result, "Local converter datetime objects are not equal")

    def test_compare_time(self):
        now = datetime.datetime.utcnow()
        assert_true = check_data_sheet.compare_times(now, datetime.datetime.utcnow())
        self.assertTrue(assert_true)
        assert_false = check_data_sheet.compare_times(now, datetime.datetime.utcnow()+datetime.timedelta(minutes=10))
        self.assertFalse(assert_false)
        assert_false2 = check_data_sheet.compare_times(now, datetime.datetime.utcnow()+datetime.timedelta(minutes=-10))
        self.assertFalse(assert_false2)
        assert_true2 = check_data_sheet.compare_times(now, datetime.datetime.utcnow()+datetime.timedelta(minutes=5))
        self.assertTrue(assert_true2)
        assert_true3 = check_data_sheet.compare_times(now, datetime.datetime.utcnow()+datetime.timedelta(minutes=-5))
        self.assertTrue(assert_true3)


if __name__ == "__main__":
    unittest.main()
