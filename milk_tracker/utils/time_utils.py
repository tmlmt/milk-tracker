from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd


def timedelta_to_hrmin(td: pd.Timedelta) -> str:
    """Convert a Pandas timedelta to a "HHhMMm" or "MMm" notation.

    Args:
    ----
        td (pd.Timestamp): The timestamp to convert

    Returns:
    -------
        str: "MMhMMm" if > 1 hr, or "MMm" otherwise

    """
    # NaN can't be converted
    if np.isnan(td.total_seconds()):
        return ""
    total_minutes = int(td.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h{minutes:02d}m" if hours > 0 else f"{minutes}m"


def is_time_format(time_string: str, time_formats: Optional[list[str]] = None) -> bool:
    """Test whether a string corresponds to a time.

    Args:
    ----
        time_string (str): string to test
        time_formats (List[str], optional): time formats to test. Defaults to ["%H:%M"].

    Returns:
    -------
        bool: result of the test

    """
    if time_formats is None:
        time_formats = ["%H:%M"]
    try:
        for time_format in time_formats:
            # Attempt to parse the string using each specified time format
            datetime.strptime(time_string, time_format)
    except ValueError:
        return False

    return True


def get_current_time(*, include_sec: bool = True) -> str:
    """Return current time.

    Parameters
    ----------
    include_sec : bool, optional
        whether to include seconds, by default True

    Returns
    -------
    str
        Current time in HH:MM or HH:MM:SS format

    """
    return f"{datetime.now():%X}" if include_sec else f"{datetime.now():%H:%M}"


def get_current_date() -> str:
    """Return current date.

    Returns
    -------
    str
        Current date in YYYY-MM-DD format

    """
    return datetime.now().date().strftime("%Y-%m-%d")
