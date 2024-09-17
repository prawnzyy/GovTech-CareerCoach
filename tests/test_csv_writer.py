import unittest

import pandas as pd

from src.csv_writer import CSV_Writer

class TestCSVWriter(unittest.TestCase):
    
    def setUp(self) -> None:
        self.writer = CSV_Writer("Test.csv")

    def test_get_file(self) -> None:
        self.assertEqual(self.writer.get_file(), "Test.csv")

    def test_set_file_fail(self) -> None:
        self.writer.set_file("NOT A CSV FILE")
        self.assertEqual(self.writer.get_file(), "Test.csv")

    def test_set_file_pass(self) -> None:
        self.writer.set_file("TestCSV.csv")
        self.assertEqual(self.writer.get_file(), "TestCSV.csv")

    def test_write(self) -> None:
        df = pd.DataFrame({
            "Event": [1, 2, 3],
            "Time": [1, 3, 4]
        })

        self.writer.write(df)
        new_df = pd.read_csv("Test.csv")
        pd.testing.assert_frame_equal(df, new_df)