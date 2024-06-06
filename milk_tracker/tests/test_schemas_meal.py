import pytest
from pydantic import ValidationError
from schemas.meal import FinishedMeal, OngoingMeal


def test_ongoing_meal_valid_data() -> None:
    """Test with valid data."""
    date = "2024-04-01"
    start_time = "12:01:00"
    meal = OngoingMeal(date=date, start_time=start_time)
    assert meal.date == date
    assert meal.start_time == start_time
    assert meal.end_time == ""


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
