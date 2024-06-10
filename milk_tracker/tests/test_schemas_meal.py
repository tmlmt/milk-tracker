from datetime import datetime

import pytest
import time_machine
from pydantic import ValidationError
from schemas.meal import FinishedMeal, Meal, MealRound, OngoingMeal
from zoneinfo import ZoneInfo


@time_machine.travel(datetime(2024, 6, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen")))
def test_default_meal() -> None:
    """Test default Meal constructor."""
    m = Meal()
    assert (m.get_start_datetime() - datetime(2024, 6, 10, 20, 50)).total_seconds() < 1


def test_ongoing_meal_valid_data() -> None:
    """Test with valid data."""
    date = "2024-04-01"
    start_time = "12:01:00"
    meal = OngoingMeal(date=date, start_time=start_time)

    # Basic info should be as input
    assert meal.date == date
    assert meal.start_time == start_time
    assert meal.end_time == ""

    # A meal round should have been automatically started
    assert len(meal.rounds) == 1
    assert str(meal.rounds[0].start_datetime.date()) == date
    assert str(meal.rounds[0].start_datetime.time()) == start_time
    assert (meal.rounds[0].end_datetime, meal.rounds[0].is_active) == (None, True)


def test_ongoing_meal_storage_data() -> None:
    """Test retrieving OngoingMeal from storage."""
    storage_data = {
        "date": "2024-06-05",
        "start_time": "16:30:00",
        "end_time": "",
        "rounds": [
            {"start_time": "2024-06-05T16:30:42.322176", "end_time": None, "is_active": True}
        ],
    }
    meal = OngoingMeal(**storage_data)
    assert meal.date == storage_data["date"]
    assert meal.start_time == storage_data["start_time"]
    assert meal.end_time == ""
    assert meal.rounds is not None
    assert len(meal.rounds) == 1


def test_ongoing_meal_invalid_data() -> None:
    """Test with expected errors."""
    # Can't give an end time
    with pytest.raises(ValidationError):
        OngoingMeal(date="2024-04-01", start_time="12:01", end_time="13:00")


def test_finished_meal_valid_data() -> None:
    """Test with valid data."""
    date = "2024-04-01"
    start_time = "12:01:00"
    end_time = "13:00:00"
    meal = FinishedMeal(date=date, start_time=start_time, end_time=end_time)
    assert meal.date == date
    assert meal.start_time == start_time
    assert meal.end_time == end_time


def test_finished_meal_invalid_data() -> None:
    """Test with expected errors."""
    # Invalid end time
    with pytest.raises(ValidationError):
        # Wrong end time
        FinishedMeal(date="2024-04-01", start_time="12:01", end_time="13:0")


@time_machine.travel(datetime(2024, 6, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen")))
def test_init_meal_round() -> None:
    """Test initiating a meal round."""
    # By default, a meal round starts now
    r = MealRound()
    assert not r.end_datetime
    assert r.is_active
    assert r.start_datetime == datetime(2024, 6, 10, 20, 50)
    # We can also specify a start time
    r = MealRound(start_datetime=datetime(2024, 5, 25, 18, 5))
    assert r.start_datetime == datetime(2024, 5, 25, 18, 5)


def test_update_meal_round() -> None:
    """Test updating meal rounds."""
    d = datetime(2024, 6, 10, 20, 50)
    r = MealRound(start_datetime=d)

    # We can update both end time and active state
    r.update(is_active=False, end_datetime=datetime(2024, 6, 10, 21, 55))
    assert not r.is_active
    assert r.end_datetime == datetime(2024, 6, 10, 21, 55)

    # We can't update an end time and keep active state
    with pytest.raises(ValidationError):
        r.is_active = True

    # We can't stop a meal without an end_time
    r = MealRound(start_datetime=d)
    with pytest.raises(ValidationError):
        r.is_active = False


def test_pause_start_meal_round() -> None:
    """Test pausing and starting meal rounds."""
    with time_machine.travel(
        datetime(2024, 6, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen"))
    ) as traveller:
        # Start meal
        m = OngoingMeal()

        # Pause after a while
        traveller.move_to(datetime(2024, 6, 10, 21, 10, 7, tzinfo=ZoneInfo("Europe/Copenhagen")))
        m.pause()
        assert m.rounds[0].model_dump() == {
            "start_datetime": datetime(2024, 6, 10, 20, 50),
            "end_datetime": datetime(2024, 6, 10, 21, 10, 7),
            "is_active": False,
        }

        # Start a new round
        traveller.move_to(datetime(2024, 6, 10, 21, 20, 10, tzinfo=ZoneInfo("Europe/Copenhagen")))
        m.start_new_round()
        assert len(m.rounds) == 2  # noqa: PLR2004
        assert m.rounds[1].model_dump() == {
            "start_datetime": datetime(2024, 6, 10, 21, 20, 10),
            "end_datetime": None,
            "is_active": True,
        }
