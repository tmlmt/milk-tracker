from pathlib import Path

import pandas as pd
from schemas.memory import Memory


class MemoriesDataModel:
    """Holds the big data table as a Pandas DataFrame."""

    def __init__(self, file_path: Path) -> None:  # noqa: D107
        self.file_path: Path = file_path
        self.load()

    def load(self) -> None:
        """Load data from excel file."""
        self.df = pd.read_csv(self.file_path)
        self.df["date"] = pd.to_datetime(self.df["date"]).dt.date

    def add(self, memory: Memory) -> None:
        """Add memory to dataset and order by date.

        Parameters
        ----------
        memory: Memory
            Memory to add to the dataset

        """
        self.df = pd.concat([self.df, memory.to_dataframe()], ignore_index=True)
        self.df = self.df.sort_values(by=["date"]).reset_index(drop=True)

    def save_to_file(self) -> None:
        """Save data back to excel file."""
        self.df.to_csv(self.file_path, index=False)
