from datetime import timedelta
from typing import Literal

from pydantic import Field, StringConstraints
from typing_extensions import Annotated
from utils.time_utils import get_current_time

from .base import UpdatableBaseModel


class ComputedValues(UpdatableBaseModel):
    """All computed values."""

    current_time: Annotated[str, StringConstraints(pattern=r"^\d{2}:\d{2}:\d{2}$")] = Field(
        default_factory=lambda: get_current_time(include_sec=True),
        description="Current time in format HH:MM:SS",
    )
    time_since_latest_end: timedelta = Field(
        default_factory=lambda: timedelta(0),
        description="Time since latest end of meal",
    )
    time_since_latest_start: timedelta = Field(
        default_factory=lambda: timedelta(0),
        description="Time since latest start of meal"
    )  # fmt: skip
    latest_meal_info: str = Field(
        default="No info",
        description="Latest meal information"
    )  # fmt: skip
    is_ongoing_meal: bool = Field(
        default=False,
        description="Lock state for input field of start of new meal"
    )  # fmt: skip
    is_ongoing_meal_paused: bool = Field(
        default=False,
        description="Whether a ongoing meal is paused"
    )  # fmt: skip
    is_ongoing_meal_buttontxt: Literal["Pause", "New round"] = Field(
        default="Pause",
        description="Button label for ongoing meal"
    )  # fmt: skip
    timer_meal_round: Annotated[str, StringConstraints(pattern=r"^(\d{2}:)?\d{2}:\d{2}$")] = Field(
        default="00:00",
        description="Timer for meal round in format HH:mm",
    )  # fmt: skip
    has_mother_taken_vitamins_today: bool = Field(
        default=False,
        description="Whether the mother has taken her vitamins today"
    )  # fmt: skip
    has_baby_taken_vitamins_today: bool = Field(
        default=False,
        description="Weather baby has taken their vitamins today"
    )  # fmt: skip
