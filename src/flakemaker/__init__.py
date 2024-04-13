import time
import threading
from datetime import datetime, timezone


class SnowflakeGenerator:
    def __init__(self, epoch=1704067200000):
        """
        Create a new SnowflakeGenerator.
        :param epoch: Milliseconds since 1970. Defaults to 1704067200000 (January 1st, 2024)
        """
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _get_timestamp(self):
        # Current time in milliseconds minus the custom epoch
        return int(time.time() * 1000) - self.epoch

    def _wait_for_next_millisecond(self, last_timestamp):
        timestamp = self._get_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_timestamp()
        return timestamp

    def generate(self, parameter):
        if parameter > 1023 or parameter < 0:  # 10 bits for parameter
            raise ValueError("Parameter must be between 0 and 1023.")

        with self.lock:
            timestamp = self._get_timestamp()

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & 0xFFF  # Increment sequence
                if self.sequence == 0:
                    timestamp = self._wait_for_next_millisecond(timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            # Shift and OR bits to form the snowflake
            snowflake = ((timestamp << 22)
                         | (parameter << 12)
                         | self.sequence)

            return snowflake

    def parse(self, snowflake):
        timestamp = (snowflake >> 22) + self.epoch
        # Convert timestamp from milliseconds to seconds for datetime
        dt = datetime.fromtimestamp(timestamp / 1000.0, tz=timezone.utc)
        parameter = (snowflake & 0x3FF000) >> 12
        return dt, parameter