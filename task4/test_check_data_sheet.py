import unittest
import sys
import check_data_sheet
from unittest.mock import patch


class TestCheckDataSheet(unittest.TestCase):

    def test_last_row(self):
        test_args = ["check_data_sheet.py"]
        with patch.object(sys, 'argv', test_args):
            check_data_sheet.main()
            self.assertIsNotNone(check_data_sheet.last_row, "Sheet's last row is None!")


if __name__ == "__main__":
    unittest.main()
