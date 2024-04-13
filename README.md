# flakemaker

The `flakemaker` library offers a straightforward approach to generating unique, time-based identifiers similar to Discord's snowflake IDs, but repurposing the worker and process IDs into a generalized "parameter".

## Features

- Generates 64-bit snowflake IDs.
- Customizable epoch.
- Includes a user-defined parameter at snowflake generation. *Note that this replaces the worker and process ids!*

## Quickstart

### Generating a Snowflake

To generate a snowflake, create an instance of `SnowflakeGenerator` and call the `generate` method with your parameter.

```python
from flakemaker import SnowflakeGenerator

generator = SnowflakeGenerator() # you can put a time here in milliseconds since 1970
snowflake = generator.generate(42) # or any value from 0-1023
print(f"Generated snowflake: {snowflake}")
# Generated snowflake: 17359567945990144
```

### Parsing a Snowflake

To parse an existing snowflake and extract its creation time and parameter, use the `parse` method.

```python
dt, parameter = generator.parse(snowflake)
print(f"Timestamp: {dt}, Parameter: {parameter}")
# Timestamp: datetime.datetime(2024, 2, 17, 13, 49, 13, 466377), Parameter: 42
```

This method returns the timestamp of the snowflake as a `datetime` object in UTC and the parameter encoded within the snowflake.
