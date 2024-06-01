import numpy as np
import pandas as pd
from datetime import datetime


def timedelta_to_hrmin(td: pd.Timedelta) -> str:
    """Converts a Pandas timedelta to a "HHhMMm" or "MMm" notation

    Args:
        td (pd.Timestamp): The timestamp to convert

    Returns:
        str: "MMhMMm" if > 1 hr, or "MMm" otherwise
    """
    # NaN can't be converted
    if np.isnan(td.total_seconds()):
        return ""
    total_minutes = int(td.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h{minutes:02d}m" if hours > 0 else f"{minutes}m"


def is_time_format(time_string: str, time_formats: list[str] = ["%H:%M"]) -> bool:
    """Tests whether a string corresponds to a time

    Args:
        time_string (str): string to test
        time_formats (_type_, optional): time formats to test. Defaults to ["%H:%M"].

    Returns:
        bool: result of the test
    """
    for time_format in time_formats:
        try:
            # Attempt to parse the string using each specified time format
            datetime.strptime(time_string, time_format)
            return True
        except ValueError:
            continue
    # If none of the formats matched, return False
    return False
