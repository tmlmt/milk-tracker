import re
from datetime import datetime, timedelta
from typing import Literal, Optional

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


def timedelta_to_timer(td: timedelta) -> str:
    """Convert a timedelta to a string in %H:%M:%S format.

    Parameters
    ----------
    td : timedelta
        Timedelta to convert

    Returns
    -------
    str
        Time in [%H:]%M:%S format

    """
    # NaN can't be converted
    if np.isnan(td.total_seconds()):
        return ""
    hours, remainder = divmod(int(td.total_seconds()), 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return (
        f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        if hours > 0
        else f"{minutes:02d}:{seconds:02d}"
    )


def time_between(after_datetime: datetime, before_datetime: datetime) -> str:
    """Return time elapsed between two datetimes.

    Parameters
    ----------
    after_datetime : datetime
        Later boundary
    before_datetime : datetime
        Earlier boundary

    Returns
    -------
    str
        Time string in [%H:]%M:%S format

    Raises
    ------
    ValueError
        If wrong order given

    """
    if after_datetime < before_datetime:
        msg = "Check order in which you input the dates when using the time_between() function"
        raise ValueError(msg)
    return timedelta_to_timer(after_datetime - before_datetime)


def time_since(since_time: datetime) -> str:
    """Return time elapsed since input datetime.

    Parameters
    ----------
    since_time : datetime
        Input datetime

    Returns
    -------
    str
        Time in [%H:]%M:%S format

    """
    return time_between(datetime.now(), since_time)


def is_same_minute(dt1: datetime, dt2: Optional[datetime] = None) -> bool:
    """Check whether two datetime values are within the same minute.

    Parameters
    ----------
    dt1 : datetime
        First datetime to compare
    dt2 : datetime, optional
        Second datetime to compare, by default now

    Returns
    -------
    bool
        Check result

    """
    if not dt2:
        dt2 = datetime.now()
    return (
        dt1.year == dt2.year
        and dt1.month == dt2.month
        and dt1.day == dt2.day
        and dt1.hour == dt2.hour
        and dt1.minute == dt2.minute
    )


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
    if time_format in ["short", "any"] and re.match(
        r"([01]\d|2[0-3]):([0-5]\d)$", test_string
    ):
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


def is_today(test_date: str) -> bool:
    """Test whether a date is today's date.

    Parameters
    ----------
    test_date : str
        Date to test in %Y-%m-%d format

    Returns
    -------
    bool
        True or False

    """
    return get_current_date() == test_date


def is_before_end_of_tomorrow(df: datetime) -> bool:
    """Check whether a datetime is before the end of tomorrow.

    Parameters
    ----------
    df : datetime
        Datetime to test

    Returns
    -------
    bool
        True or False

    """
    end_of_tomorrow = (datetime.now() + timedelta(days=2)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return df < end_of_tomorrow
