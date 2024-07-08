from datetime import date

import pandas as pd
from pydantic import BaseModel, Field


class Memory(BaseModel):
    """Base model for meals."""

    date_field: date = Field(default_factory=date.today, description="Date", alias="date")
    description: str = Field(default="", description="Description of the memory")

    def to_dataframe(self) -> pd.DataFrame:
        """Convert Memory into a Dataframe entry."""
        return pd.DataFrame(
            data={"date": [self.date_field], "description": [self.description]}
        )
