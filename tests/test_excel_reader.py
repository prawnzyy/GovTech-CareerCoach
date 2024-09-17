import unittest
from unittest.mock import patch

import pandas as pd

from src.excel_reader import Excel_Reader

class TestExcelReader(unittest.TestCase):

    @patch("pandas.read_excel")
    def setUp(self, mock_read_excel) -> None:
        self.excel_reader = Excel_Reader("https://mockexcel.com/test.xlsx")

    @patch("pandas.read_excel")
    def test_get_url(self, mock_read_excel) -> None:
        self.assertEqual(self.excel_reader.get_url(), "https://mockexcel.com/test.xlsx")

    @patch("pandas.read_excel")
    def test_set_url(self, mock_read_excel) -> None:
        self.excel_reader.set_url("https://mockexcel.com/testsecond.xlsx")
        self.assertEqual(self.excel_reader.get_url(), "https://mockexcel.com/testsecond.xlsx")

    @patch("pandas.read_excel")
    def test_get_df(self, mock_read_excel) -> None:
        mock_df = pd.DataFrame({
            "Event": ["Event A", "Event B"],
            "Time": ["10-10-10", "08-08-08"]
        })

        mock_read_excel.return_value = mock_df

        self.excel_reader = Excel_Reader("This is a test url")

        result_df = self.excel_reader.get_df()
        pd.testing.assert_frame_equal(result_df, mock_df)

if __name__ == "__main__":
    unittest.main()