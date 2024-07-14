from datetime import date
from pathlib import Path

import pandas as pd
from schemas.memory import Memory
from utils.time_utils import days_between_txt


class MemoriesDataModel:
    """Holds the big data table as a Pandas DataFrame."""

    def __init__(self, file_path: Path, birthday: date) -> None:  # noqa: D107
        self.file_path: Path = file_path
        self.load()
        self._birthday = birthday
        self.compute_extra_columns()
        self.compute_table_rows()

    def load(self) -> None:
        """Load data from excel file."""
        self.df = pd.read_csv(self.file_path)
        self.df["date"] = pd.to_datetime(self.df["date"]).dt.date
        self.df = self.df.sort_values(by=["date"], ascending=False).reset_index(drop=True)

    def compute_table_rows(self) -> None:
        """Generate rows to insert in NiceGUI table element."""
        self.table_rows = self.df.to_dict("records")

    def compute_extra_columns(self) -> None:
        """Generate 'index' and 'age' columns."""
        self.df["index"] = self.df.index
        self.df["age"] = self.df["date"].apply(
            lambda x: days_between_txt(x, self._birthday)
        )

    def add(self, memory: Memory) -> None:
        """Add memory to dataset and order by date.

        Parameters
        ----------
        memory: Memory
            Memory to add to the dataset

        """
        self.df = pd.concat([self.df, memory.to_dataframe()], ignore_index=True)
        self.df = self.df.sort_values(by=["date"], ascending=False).reset_index(drop=True)
        self.compute_extra_columns()
        self.compute_table_rows()

    def remove(self, index: int) -> None:
        """Delete memory based on its index in the dataframe.

        Parameters
        ----------
        index : int
            index to delete

        """
        self.df = self.df.drop(index).reset_index(drop=True)
        self.compute_extra_columns()
        self.compute_table_rows()

    def edit(self, index: int, memory: Memory) -> None:
        """Update memory at a specific index.

        Parameters
        ----------
        index : int
            index to update
        memory : Memory
            edited Memory

        """
        for key, value in memory.to_dict().items():
            self.df.loc[index, key] = value
        self.compute_extra_columns()
        self.compute_table_rows()

    def save_to_file(self) -> None:
        """Save data back to excel file."""
        self.df[["date", "description"]].to_csv(self.file_path, index=False)
