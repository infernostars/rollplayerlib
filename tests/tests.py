import time
import unittest
from datetime import datetime

from src.flakemaker import SnowflakeGenerator

class TestSnowflakeGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = SnowflakeGenerator()

    def test_snowflake_generation_and_parsing(self):
        parameter = 512
        snowflake = self.generator.generate(parameter)
        parsed_dt, parsed_parameter = self.generator.parse(snowflake)

        self.assertIsInstance(parsed_dt, datetime)
        self.assertEqual(parsed_parameter, parameter)

    def test_sequence_incrementation(self):
        parameter = 100
        first_snowflake = self.generator.generate(parameter)
        second_snowflake = self.generator.generate(parameter)

        # Ensure the sequence increments, implying the second snowflake is greater
        self.assertTrue(second_snowflake > first_snowflake)

    def test_timestamp_change(self):
        parameter = 42
        first_snowflake = self.generator.generate(parameter)
        time.sleep(0.002)  # Sleep for 2 milliseconds to ensure a timestamp change
        second_snowflake = self.generator.generate(parameter)

        first_timestamp, _ = self.generator.parse(first_snowflake)
        second_timestamp, _ = self.generator.parse(second_snowflake)

        # Ensure the timestamps are different
        self.assertNotEqual(first_timestamp, second_timestamp)


if __name__ == '__main__':
    unittest.main()