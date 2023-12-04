import unittest
import pytest
import pandas as pd
from scibatt.readers import maccor
import os


class TestMaccor(unittest.TestCase):
    def test_read_txt_with_valid_datafile(self):
        data_file_path = os.path.join(
            os.path.dirname(__file__), "test_data", "maccor.txt"
        )
        data = maccor.read_txt(data_file_path)

        self.assertIsInstance(data, dict)
        # self.assertEqual(df.shape, (10, 10))

        print(data)


if __name__ == "__main__":
    unittest.main()
