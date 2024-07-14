from datetime import date, datetime, timedelta

import pytest
import time_machine
from utils.time_utils import (
    days_between_int,
    days_between_txt,
    force_full_time,
    is_before_end_of_tomorrow,
    is_same_minute,
    is_time_format,
    is_today,
    time_between,
    time_since,
    timedelta_to_timer,
)
from zoneinfo import ZoneInfo


def test_valid_time() -> None:
    """Test that should all pass."""
    assert is_time_format("14:01")
    assert is_time_format("14:01", "short")
    assert is_time_format("14:00:01")
    assert is_time_format("14:00:01", "full")


def test_invalid_short_time() -> None:
    """Test that should fail with short format."""
    assert not is_time_format("14:0", "short")
    assert not is_time_format("14:000", "short")
    assert not is_time_format("14-00", "short")
    assert not is_time_format("25:01", "short")
    assert not is_time_format("14:70", "short")
    assert not is_time_format("     ", "short")
    assert not is_time_format("", "short")
    assert not is_time_format(" ", "short")


def test_invalid_full_time() -> None:
    """Test that should fail with full format."""
    assert not is_time_format("14:00", "full")
    assert not is_time_format("14:01:0", "full")
    assert not is_time_format("14:01:011", "full")
    assert not is_time_format("25:01:01", "full")
    assert not is_time_format("14:70:01", "full")
    assert not is_time_format("        ", "full")
    assert not is_time_format("", "full")
    assert not is_time_format(" ", "full")


def test_force_full_time() -> None:
    """Test force_full_time()."""
    assert force_full_time("17:41") == "17:41:00"
    assert force_full_time("17:01:01") == "17:01:01"
    with pytest.raises(TypeError):
        force_full_time("17:0")
    with pytest.raises(TypeError):
        force_full_time("17h01")


def test_timedelta_to_timer() -> None:
    """Test timedelta_to_timer()."""
    assert timedelta_to_timer(timedelta(hours=1, minutes=23, seconds=4)) == "01:23:04"
    assert timedelta_to_timer(timedelta(hours=0, minutes=23, seconds=4)) == "23:04"


@time_machine.travel(datetime(2024, 6, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen")))
def test_time_since() -> None:
    """Test time_since()."""
    now = datetime.now()
    assert (now.hour, now.minute) == (20, 50)
    assert time_since(datetime.now()) == "00:00"
    assert time_since(datetime(2024, 6, 10, 20, 50)) == "00:00"
    assert time_since(datetime(2024, 6, 10, 20, 30, 35)) == "19:25"
    assert time_since(datetime(2024, 6, 10, 18, 45)) == "02:05:00"


def test_time_between() -> None:
    """Test time_between()."""
    assert (
        time_between(datetime(2024, 6, 10, 21, 52), datetime(2024, 6, 10, 20, 50))
        == "01:02:00"
    )
    assert (
        time_between(datetime(2024, 6, 10, 21, 52, 12), datetime(2024, 6, 10, 21, 50, 6))
        == "02:06"
    )


def test_is_same_minute() -> None:
    """Test is_same_minute()."""
    assert is_same_minute(
        datetime(2024, 6, 10, 21, 52), datetime(2024, 6, 10, 21, 52, 16)
    )
    assert not is_same_minute(
        datetime(2024, 6, 10, 21, 52), datetime(2024, 6, 10, 21, 51, 16)
    )
    with time_machine.travel(
        datetime(2024, 5, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen"))
    ):
        assert is_same_minute(datetime(2024, 5, 10, 20, 50, 25))
        assert not is_same_minute(datetime(2024, 5, 10, 20, 49, 25))


@time_machine.travel(datetime(2024, 6, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen")))
def test_is_today() -> None:
    """Test is_today()."""
    assert is_today("2024-06-10")
    assert not is_today("2024-06-11")


@time_machine.travel(datetime(2024, 6, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen")))
def test_is_before_end_of_tomorrow() -> None:
    """Test is_before_end_of_tomorrow()."""
    assert is_before_end_of_tomorrow(datetime(2024, 6, 9, 12, 15))
    assert is_before_end_of_tomorrow(datetime(2024, 6, 10, 23, 15))
    assert is_before_end_of_tomorrow(datetime(2024, 6, 11, 22, 15))
    assert is_before_end_of_tomorrow(datetime(2024, 6, 11, 23, 59))
    assert not is_before_end_of_tomorrow(datetime(2024, 6, 12, 0, 0, 0))
    assert not is_before_end_of_tomorrow(datetime(2024, 6, 12, 0, 1))


def test_days_between() -> None:
    """Test days_between_int() and days_between_txt()."""
    assert days_between_int(date(2024, 1, 1), date(2024, 1, 1)) == 0
    assert days_between_txt(date(2024, 1, 1), date(2024, 1, 1)) == "0 day"
    assert days_between_int(date(2024, 1, 1), date(2024, 1, 8)) == 7  # noqa: PLR2004
    assert days_between_txt(date(2024, 1, 1), date(2024, 1, 8)) == "1 week"
    assert days_between_int(date(2024, 1, 1), date(2024, 1, 17)) == 16  # noqa: PLR2004
    assert days_between_txt(date(2024, 1, 1), date(2024, 1, 17)) == "2 weeks 2 days"
    assert days_between_int(date(2024, 1, 1), date(2024, 2, 1)) == 31  # noqa: PLR2004
    assert days_between_txt(date(2024, 1, 1), date(2024, 2, 1)) == "1 month"
    assert days_between_int(date(2024, 1, 1), date(2024, 2, 25)) == 55  # noqa: PLR2004
    assert days_between_txt(date(2024, 1, 1), date(2024, 2, 25)) == "7 weeks 6 days"
    assert days_between_txt(date(2024, 1, 1), date(2024, 3, 25)) == "2 months 24 days"
    assert days_between_int(date(2023, 1, 1), date(2024, 3, 6)) == 430  # noqa: PLR2004
    assert (
        days_between_txt(date(2023, 1, 1), date(2024, 3, 6)) == "1 year 2 months 5 days"
    )
    assert (
        days_between_txt(date(2020, 1, 1), date(2024, 4, 2)) == "4 years 3 months 1 day"
    )
    # When the later date is just after new years
    assert days_between_txt(date(2023, 11, 10), date(2024, 1, 1)) == "7 weeks 3 days"
