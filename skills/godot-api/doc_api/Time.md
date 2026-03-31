## Time <- Object

The Time singleton allows converting time between various formats and also getting time information from the system. This class conforms with as many of the ISO 8601 standards as possible. All dates follow the Proleptic Gregorian calendar. As such, the day before `1582-10-15` is `1582-10-14`, not `1582-10-04`. The year before 1 AD (aka 1 BC) is number `0`, with the year before that (2 BC) being `-1`, etc. Conversion methods assume "the same timezone", and do not handle timezone conversions or DST automatically. Leap seconds are also not handled, they must be done manually if desired. Suffixes such as "Z" are not handled, you need to strip them away manually. When getting time information from the system, the time can either be in the local timezone or UTC depending on the `utc` parameter. However, the `get_unix_time_from_system` method always uses UTC as it returns the seconds passed since the . **Important:** The `_from_system` methods use the system clock that the user can manually set. **Never use** this method for precise time calculation since its results are subject to automatic adjustments by the user or the operating system. **Always use** `get_ticks_usec` or `get_ticks_msec` for precise time calculation instead, since they are guaranteed to be monotonic (i.e. never decrease).

**Methods:**
- get_date_dict_from_system(utc: bool = false) -> Dictionary - Returns the current date as a dictionary of keys: `year`, `month`, `day`, and `weekday`. The returned values are in the system's local time when `utc` is `false`, otherwise they are in UTC.
- get_date_dict_from_unix_time(unix_time_val: int) -> Dictionary - Converts the given Unix timestamp to a dictionary of keys: `year`, `month`, `day`, and `weekday`.
- get_date_string_from_system(utc: bool = false) -> String - Returns the current date as an ISO 8601 date string (YYYY-MM-DD). The returned values are in the system's local time when `utc` is `false`, otherwise they are in UTC.
- get_date_string_from_unix_time(unix_time_val: int) -> String - Converts the given Unix timestamp to an ISO 8601 date string (YYYY-MM-DD).
- get_datetime_dict_from_datetime_string(datetime: String, weekday: bool) -> Dictionary - Converts the given ISO 8601 date and time string (YYYY-MM-DDTHH:MM:SS) to a dictionary of keys: `year`, `month`, `day`, [code skip-lint]weekday[/code], `hour`, `minute`, and `second`. If `weekday` is `false`, then the [code skip-lint]weekday[/code] entry is excluded (the calculation is relatively expensive). **Note:** Any decimal fraction in the time string will be ignored silently.
- get_datetime_dict_from_system(utc: bool = false) -> Dictionary - Returns the current date as a dictionary of keys: `year`, `month`, `day`, `weekday`, `hour`, `minute`, `second`, and `dst` (Daylight Savings Time).
- get_datetime_dict_from_unix_time(unix_time_val: int) -> Dictionary - Converts the given Unix timestamp to a dictionary of keys: `year`, `month`, `day`, `weekday`, `hour`, `minute`, and `second`. The returned Dictionary's values will be the same as the `get_datetime_dict_from_system` if the Unix timestamp is the current time, with the exception of Daylight Savings Time as it cannot be determined from the epoch.
- get_datetime_string_from_datetime_dict(datetime: Dictionary, use_space: bool) -> String - Converts the given dictionary of keys to an ISO 8601 date and time string (YYYY-MM-DDTHH:MM:SS). The given dictionary can be populated with the following keys: `year`, `month`, `day`, `hour`, `minute`, and `second`. Any other entries (including `dst`) are ignored. If the dictionary is empty, `0` is returned. If some keys are omitted, they default to the equivalent values for the Unix epoch timestamp 0 (1970-01-01 at 00:00:00). If `use_space` is `true`, the date and time bits are separated by an empty space character instead of the letter T.
- get_datetime_string_from_system(utc: bool = false, use_space: bool = false) -> String - Returns the current date and time as an ISO 8601 date and time string (YYYY-MM-DDTHH:MM:SS). The returned values are in the system's local time when `utc` is `false`, otherwise they are in UTC. If `use_space` is `true`, the date and time bits are separated by an empty space character instead of the letter T.
- get_datetime_string_from_unix_time(unix_time_val: int, use_space: bool = false) -> String - Converts the given Unix timestamp to an ISO 8601 date and time string (YYYY-MM-DDTHH:MM:SS). If `use_space` is `true`, the date and time bits are separated by an empty space character instead of the letter T.
- get_offset_string_from_offset_minutes(offset_minutes: int) -> String - Converts the given timezone offset in minutes to a timezone offset string. For example, -480 returns "-08:00", 345 returns "+05:45", and 0 returns "+00:00".
- get_ticks_msec() -> int - Returns the amount of time passed in milliseconds since the engine started. Will always be positive or 0 and uses a 64-bit value (it will wrap after roughly 500 million years).
- get_ticks_usec() -> int - Returns the amount of time passed in microseconds since the engine started. Will always be positive or 0 and uses a 64-bit value (it will wrap after roughly half a million years).
- get_time_dict_from_system(utc: bool = false) -> Dictionary - Returns the current time as a dictionary of keys: `hour`, `minute`, and `second`. The returned values are in the system's local time when `utc` is `false`, otherwise they are in UTC.
- get_time_dict_from_unix_time(unix_time_val: int) -> Dictionary - Converts the given time to a dictionary of keys: `hour`, `minute`, and `second`.
- get_time_string_from_system(utc: bool = false) -> String - Returns the current time as an ISO 8601 time string (HH:MM:SS). The returned values are in the system's local time when `utc` is `false`, otherwise they are in UTC.
- get_time_string_from_unix_time(unix_time_val: int) -> String - Converts the given Unix timestamp to an ISO 8601 time string (HH:MM:SS).
- get_time_zone_from_system() -> Dictionary - Returns the current time zone as a dictionary of keys: `bias` and `name`. - `bias` is the offset from UTC in minutes, since not all time zones are multiples of an hour from UTC. - `name` is the localized name of the time zone, according to the OS locale settings of the current user.
- get_unix_time_from_datetime_dict(datetime: Dictionary) -> int - Converts a dictionary of time values to a Unix timestamp. The given dictionary can be populated with the following keys: `year`, `month`, `day`, `hour`, `minute`, and `second`. Any other entries (including `dst`) are ignored. If the dictionary is empty, `0` is returned. If some keys are omitted, they default to the equivalent values for the Unix epoch timestamp 0 (1970-01-01 at 00:00:00). You can pass the output from `get_datetime_dict_from_unix_time` directly into this function and get the same as what was put in. **Note:** Unix timestamps are often in UTC. This method does not do any timezone conversion, so the timestamp will be in the same timezone as the given datetime dictionary.
- get_unix_time_from_datetime_string(datetime: String) -> int - Converts the given ISO 8601 date and/or time string to a Unix timestamp. The string can contain a date only, a time only, or both. **Note:** Unix timestamps are often in UTC. This method does not do any timezone conversion, so the timestamp will be in the same timezone as the given datetime string. **Note:** Any decimal fraction in the time string will be ignored silently.
- get_unix_time_from_system() -> float - Returns the current Unix timestamp in seconds based on the system time in UTC. This method is implemented by the operating system and always returns the time in UTC. The Unix timestamp is the number of seconds passed since 1970-01-01 at 00:00:00, the . **Note:** Unlike other methods that use integer timestamps, this method returns the timestamp as a [float] for sub-second precision.

**Enums:**
**Month:** MONTH_JANUARY=1, MONTH_FEBRUARY=2, MONTH_MARCH=3, MONTH_APRIL=4, MONTH_MAY=5, MONTH_JUNE=6, MONTH_JULY=7, MONTH_AUGUST=8, MONTH_SEPTEMBER=9, MONTH_OCTOBER=10, ...
  - MONTH_JANUARY: The month of January, represented numerically as `01`.
  - MONTH_FEBRUARY: The month of February, represented numerically as `02`.
  - MONTH_MARCH: The month of March, represented numerically as `03`.
  - MONTH_APRIL: The month of April, represented numerically as `04`.
  - MONTH_MAY: The month of May, represented numerically as `05`.
  - MONTH_JUNE: The month of June, represented numerically as `06`.
  - MONTH_JULY: The month of July, represented numerically as `07`.
  - MONTH_AUGUST: The month of August, represented numerically as `08`.
  - MONTH_SEPTEMBER: The month of September, represented numerically as `09`.
  - MONTH_OCTOBER: The month of October, represented numerically as `10`.
  - MONTH_NOVEMBER: The month of November, represented numerically as `11`.
  - MONTH_DECEMBER: The month of December, represented numerically as `12`.
**Weekday:** WEEKDAY_SUNDAY=0, WEEKDAY_MONDAY=1, WEEKDAY_TUESDAY=2, WEEKDAY_WEDNESDAY=3, WEEKDAY_THURSDAY=4, WEEKDAY_FRIDAY=5, WEEKDAY_SATURDAY=6
  - WEEKDAY_SUNDAY: The day of the week Sunday, represented numerically as `0`.
  - WEEKDAY_MONDAY: The day of the week Monday, represented numerically as `1`.
  - WEEKDAY_TUESDAY: The day of the week Tuesday, represented numerically as `2`.
  - WEEKDAY_WEDNESDAY: The day of the week Wednesday, represented numerically as `3`.
  - WEEKDAY_THURSDAY: The day of the week Thursday, represented numerically as `4`.
  - WEEKDAY_FRIDAY: The day of the week Friday, represented numerically as `5`.
  - WEEKDAY_SATURDAY: The day of the week Saturday, represented numerically as `6`.

