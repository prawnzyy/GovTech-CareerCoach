import unittest
from unittest.mock import patch

import pandas as pd

from src.json_reader import Json_Reader

class TestJsonReader(unittest.TestCase):

    @patch("urllib.request.urlopen")
    @patch("json.load")
    @patch("pandas.json_normalize")
    @patch("pandas.read_json")
    def setUp(self, mock_read_json, mock_json_normalize, mock_json_load, mock_urllib_request_urlopen) -> None:
        self.json_reader = Json_Reader("https://mockexcel.com/test.xlsx")

    def test_get_url(self) -> None:
        self.assertEqual(self.json_reader.get_url(), "https://mockexcel.com/test.xlsx")

    @patch("urllib.request.urlopen")
    @patch("json.load")
    @patch("pandas.json_normalize")
    @patch("pandas.read_json")
    def test_set_url(self, mock_read_json, mock_json_normalize, mock_json_load, mock_urllib_request_urlopen) -> None:
        self.json_reader.set_url("https://mockexcel.com/testsecond.xlsx")
        self.assertEqual(self.json_reader.get_url(), "https://mockexcel.com/testsecond.xlsx")

    @patch("urllib.request.urlopen")
    @patch("json.load")
    @patch("pandas.json_normalize")
    @patch("pandas.read_json")
    def test_get_normal_df(self, mock_read_json, mock_json_normalize, mock_json_load, mock_urllib_request_urlopen) -> None:
        mock_df = pd.DataFrame({
            "Event": ["Event A", "Event B"],
            "Time": ["10-10-10", "08-08-08"]
        })

        mock_read_json.return_value = mock_df

        self.json_reader = Json_Reader("This is a test url")

        result_df = self.json_reader.get_df()
        pd.testing.assert_frame_equal(result_df, mock_df)

    @patch("urllib.request.urlopen")
    @patch("json.load")
    @patch("pandas.json_normalize")
    @patch("pandas.read_json")
    def test_get_flatten_df(self, mock_read_json, mock_json_normalize, mock_json_load, mock_urllib_request_urlopen) -> None:
        mock_df = pd.DataFrame({
            "restaurants": [{"Name": "Test"}],
        })

        mock_json_normalize.return_value = mock_df

        self.json_reader = Json_Reader("This is a test url")

        result_df = self.json_reader.get_restaurant_df()
        pd.testing.assert_frame_equal(result_df, mock_df)
        
if __name__ == "__main__":
    unittest.main()