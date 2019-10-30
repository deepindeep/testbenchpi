import sys
import unittest
import json
from unittest.mock import patch
import insert_row
import utils


class TestInsertRow(unittest.TestCase):

    def test_insert_row(self):
        test_args = ["insert_row.py"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(utils.InvalidParamsException):
                insert_row.main()
        test_args = ["insert_row.py", "https://google.com"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(utils.InvalidParamsException):
                insert_row.main()
        test_args = ["insert_row.py", "invalid_url", 1488]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(utils.InvalidURLException):
                insert_row.main()
        test_args = ["insert_row.py", "https://www.google.com/", 7.40]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(utils.SheetIDNotFoundException):
                insert_row.main()

    def test_insert_data(self):
        test_args = ["insert_row.py",
                     "https://docs.google.com/spreadsheets/d/1UUyGns2Fhyy-C2LTJtrJIzXrqdQ2kd5OrHUDXbRFDYU/edit#gid=0",
                     "data"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(json.decoder.JSONDecodeError):
                insert_row.main()
        test_args = ["insert_row.py",
                     "https://docs.google.com/spreadsheets/d/1UUyGns2Fhyy-C2LTJtrJIzXrqdQ2kd5OrHUDXbRFDYU/edit#gid=0",
                     '{"a": 1, "b": 2, "c": 3}']
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(utils.InvalidDataColumnException):
                insert_row.main()

    def test_create_service(self):
        service = utils.build_sheet_service()
        self.assertIsNotNone(service)

    # def test_google_sheet(self):
    #     test_args = ["insert_row.py", "https://docs.google.com/spreadsheets/d/1UUyGns2Fhyy-C2LTJtrJIzXrqdQ2kd5OrHUDXbRFDYU/edit#gid=0", 666]


if __name__ == "__main__":
    unittest.main()
