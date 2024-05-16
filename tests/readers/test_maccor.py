import unittest
from scibatt.readers import maccor
import os


class TestMaccor(unittest.TestCase):
    def test_read_txt_with_valid_datafile(self):
        data_file_path = os.path.join(
            os.path.dirname(__file__), "test_data", "maccor.txt"
        )
        data = maccor.read_txt(data_file_path)

        self.assertIsInstance(data, dict)

    def test_read_csv_with_valid_datafile(self):
        data_file_path = os.path.join(
            os.path.dirname(__file__), "test_data", "maccor.csv"
        )
        data = maccor.read_csv(data_file_path)

        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
