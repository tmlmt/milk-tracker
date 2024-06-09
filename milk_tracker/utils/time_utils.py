import re
from datetime import datetime
from typing import List, Literal, Optional

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


def timedelta_to_float(td: pd.Timedelta, unit: Literal["m", "h"]) -> float:
    """Convert a Pandas timedelta as float.

    Args:
    ----
        td (pd.Timestamp): The timestamp to convert
        unit (Literal["m", "h"]): Either to convert in minutes or hours

    Returns:
    -------
        float: corresponding minutes or hours

    """
    # NaN can't be converted
    if np.isnan(td.total_seconds()):
        return np.nan
    if unit == "m":
        return td.total_seconds() / 60
    return td.total_seconds() / 3600


def is_time_format(
    test_string: str, time_format: Optional[Literal["short", "full", "any"]] = "any"
) -> bool:
    """Test whether a string corresponds to a time.

    Parameters
    ----------
    test_string : str
        String to test
    time_format : Optional[Literal["short", "full", "any"]], optional
        _description_, by default "short"

    Returns
    -------
    bool
        Test result

    """
    if time_format in ["short", "any"] and re.match(r"([01]\d|2[0-3]):([0-5]\d)$", test_string):
        return True
    if time_format in ["full", "any"] and re.match(
        r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$", test_string
    ):
        return True
    return False


def force_full_time(time_string: str) -> str:
    """Force a time string in full format HH:mm:ss with 00 at the end.

    Parameters
    ----------
    time_string : str
        Input string

    Returns
    -------
    str
        Time string in full format

    Raises
    ------
    TypeError
        If input string not a valid time format

    """
    if not is_time_format(time_string):
        msg = "Input string must be a valid time format"
        raise TypeError(msg)
    if len(time_string) == 5:  # noqa: PLR2004
        return time_string + ":00"
    return time_string


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
