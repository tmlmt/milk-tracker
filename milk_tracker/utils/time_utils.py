import re
from datetime import date, datetime, timedelta
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
    return bool(
        (
            time_format in ["short", "any"]
            and re.match(r"([01]\d|2[0-3]):([0-5]\d)$", test_string)
        )
        or (
            time_format in ["full", "any"]
            and re.match(r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$", test_string)
        )
    )


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


def days_between_int(date1: date, date2: date) -> int:
    """Calculate the number of days between two dates.

    Parameters
    ----------
    date1 : date
        first date
    date2 : date
        second date

    Returns
    -------
    int
        number of days (starts at 1)

    """
    # Ensure date1 is earlier than date2
    if date1 > date2:
        date1, date2 = date2, date1
    return int(np.floor((date2 - date1).total_seconds() / (24 * 60 * 60)))


def days_between_txt(date1: date, date2: date) -> str:
    """Return the time period between two dates.

    Parameters
    ----------
    date1 : date
        first date
    date2 : date
        second date

    Returns
    -------
    str
        Time period in format [y year(s) ][m month(s) ]d day(s)

    """
    # Ensure date1 is earlier than date2
    if date1 > date2:
        date1, date2 = date2, date1

    # Calculate the difference in years, months, and days
    years = date2.year - date1.year
    months = date2.month - date1.month
    days = date2.day - date1.day
    weeks = 0

    # Adjust for negative months and days
    if days < 0:
        months -= 1
        days += (date2.replace(day=1) - date2.replace(month=date2.month - 1, day=1)).days

    if months < 0:
        years -= 1
        months += 12

    # Construct the output string
    result = []
    if years:
        result.append(f"{years} year{'s' if years > 1 else ''}")
    if months and (months >= 2 or days < 7):  # noqa: PLR2004
        result.append(f"{months} month{'s' if months > 1 else ''}")
    elif (not months and days > 0) or (months and months) == 1:
        weeks = (
            days_between_int(
                date(2024, date1.month, date1.day), date(2024, date2.month, date2.day)
            )
            // 7
        )
        days = days_between_int(
            date(2024, date1.month, date1.day) + timedelta(weeks=weeks),
            date(2024, date2.month, date2.day),
        )
        result.append(f"{weeks} week{'s' if weeks > 1 else ''}")
    if days or not (years or months or weeks or days):
        result.append(f"{days} day{'s' if days > 1 else ''}")

    return " ".join(result)
