import re
from datetime import datetime
from typing import List, Optional, Self

import pandas as pd
from pydantic import BaseModel, Field, field_validator, model_validator
from utils.time_utils import force_full_time, get_current_date, get_current_time, is_time_format

from .base import UpdatableBaseModel


class Meal(BaseModel):
    """Base model for meals."""

    date: str = Field(
        default_factory=lambda: get_current_date(),
        description="Date in format YYYY-MM-DD"
    )  # fmt: skip
    start_time: str = Field(
        default_factory=lambda: get_current_time(include_sec=True),
        description="Start time in format HH:mm:ss",
    )
    end_time: Optional[str] = Field(
        default="",
        description="End time in format HH:mm:ss"
    )  # fmt: skip

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:  # noqa: D102
        if not re.match(r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", v):
            msg = "date must be in format YYYY-MM-DD"
            raise ValueError(msg)
        return v

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, v: str) -> str:  # noqa: D102
        if not is_time_format(v):
            msg = "start_time must be in HH:mm[:ss]"
            raise ValueError(msg)
        return force_full_time(v)

    def get_start_datetime(self) -> pd.Timestamp:
        """Return start date and time in datetime format.

        Returns
        -------
        pd.Timestamp
            Start date and time

        """
        return pd.to_datetime(str(self.date) + " " + str(self.start_time))


class MealRound(UpdatableBaseModel):
    """Round of meal."""

    start_time: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Start datetime of round"
    )  # fmt: skip
    end_time: Optional[datetime] = Field(default=None, description="End datetime of round")
    is_active: bool = Field(
        default=True,
        description="Whether the round is active"
    )  # fmt: skip

    @model_validator(mode="after")
    def check_end_time_or_active(self) -> Self:
        """Check mutual exclusivity of end_time and is_active."""
        if self.is_active and self.end_time:
            msg = "There must be no end_time if the round is active"
            raise ValueError(msg)
        if not self.is_active and not self.end_time:
            msg = "There must be an end_time if the round is no longer active"
            raise ValueError(msg)
        return self


class OngoingMeal(Meal, UpdatableBaseModel):
    """Meal that started at a certain date and start_time but without end_time yet.

    Raises
    ------
    ValueError
        If end_time is provided or not empty

    """

    rounds: Optional[List[MealRound]] = Field(
        default_factory=lambda: [MealRound()], description="List of meal rounds"
    )
    "List of rounds"

    @field_validator("end_time")
    @classmethod
    def validate_empty_end_time(cls, v: Optional[str]) -> Optional[str]:  # noqa: D102
        if v is not None and v != "":
            msg = "end_time must not be provided or be empty for OngoingMeal"
            raise ValueError(msg)
        return v


class FinishedMeal(Meal):
    """Meal that started at a certain date and start_time and ended at end_time."""

    end_time: str = Field(..., description="End time in format HH:mm")

    @field_validator("end_time")
    @classmethod
    def validate_non_empty_end_time(cls, v: str) -> str:  # noqa: D102
        if not is_time_format(v):
            msg = "end_time must be in HH:mm[:ss]"
            raise ValueError(msg)
        return force_full_time(v)
