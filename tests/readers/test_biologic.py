import unittest
import pytest
import pandas as pd
from scibatt.readers import biologic
import os


class TestBioLogic(unittest.TestCase):
    def test_read_txt_with_valid_datafile(self):
        data_file_path = os.path.join(
            os.path.dirname(__file__), "test_data", "biologic.mpr"
        )
        data = biologic.read_mpr(data_file_path)

        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
