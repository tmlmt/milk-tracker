from datetime import timedelta

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
