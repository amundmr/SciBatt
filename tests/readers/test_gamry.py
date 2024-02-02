import unittest
from scibatt.readers import gamry
import os


class TestGamry(unittest.TestCase):
    def test_read_dta_with_valid_datafile(self):
        data_file_path = os.path.join(
            os.path.dirname(__file__), "test_data", "gamry.DTA"
        )
        data = gamry.read_dta(data_file_path)

        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
