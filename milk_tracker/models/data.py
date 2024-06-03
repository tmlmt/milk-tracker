from pathlib import Path
from typing import List

import pandas as pd
from utils.time_utils import timedelta_to_hrmin


class DataModel:
    """Holds the big data table as a Pandas DataFrame."""

    def __init__(self, file_path: Path) -> None:  # noqa: D107
        self.file_path: Path = file_path
        self.base_fields: List[str] = ["date", "start_time", "end_time"]
        self.df: pd.DataFrame = pd.read_excel(file_path)
        self.load()

    def load(self) -> None:
        """Load data from excel file."""
        self.df = pd.read_excel(self.file_path)
        self.clean()
        self.prepare()

    def clean(self) -> None:
        """Fill gaps and convert to datetime."""
        # When there's no end_time, make it equal to start time
        self.df.loc[self.df["end_time"] == "?", "end_time"] = self.df["start_time"]
        # Turn date and time columns to datetime
        self.df["date"] = pd.to_datetime(self.df["date"])

    def prepare(self) -> None:
        """Prepare dataset before first use."""
        self.df = self.compute_columns(self.df)

    def compute_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate other columns.

        Parameters
        ----------
        df : pd.DataFrame
            Unprocessed dataset only containing base fields

        Returns
        -------
        pd.DataFrame
            Dataset containing other required columns for analysis

        """
        # Combine 'Date' and 'Time' into a single datetime column
        # Convert to string first and combine, to circumvent errors
        # in converting excel format to datetime
        df["start_datetime"] = df.apply(
            lambda row: pd.to_datetime(str(row["date"].date()) + " " + str(row["start_time"])),
            axis=1,
        )
        df["end_datetime"] = df.apply(
            lambda row: pd.to_datetime(str(row["date"].date()) + " " + str(row["end_time"])),
            axis=1,
        )

        df.loc[df["end_datetime"] < df["start_datetime"], "end_datetime"] += pd.Timedelta(days=1)

        # Calculate duration
        df["duration"] = df["end_datetime"] - df["start_datetime"]
        df["duration_hrmin"] = df["duration"].apply(timedelta_to_hrmin)
        df["duration_min"] = round(df["duration"].dt.total_seconds() / 60, 2)

        # Calculate other things of interest
        df["previous_end_datetime"] = df["end_datetime"].shift(1)
        df["time_since_previous_start"] = df["start_datetime"].diff()
        df["time_since_previous_start_hrmin"] = df["time_since_previous_start"].apply(
            timedelta_to_hrmin
        )
        df["time_since_previous_start_hrs"] = round(
            df["time_since_previous_start"].dt.total_seconds() / 3600, 2
        )

        df["time_since_previous_end"] = df["start_datetime"] - df["previous_end_datetime"]
        df["time_since_previous_end_hrmin"] = df["time_since_previous_end"].apply(
            timedelta_to_hrmin
        )
        df["time_since_previous_end_hrs"] = round(
            df["time_since_previous_end"].dt.total_seconds() / 3600, 2
        )

        return df

    def add(self, date: str, start_time: str, end_time: str) -> None:
        """Add meal to dataset.

        Parameters
        ----------
        date : str
            Date YYYY-MM-DD
        start_time : str
            Start time HH:MM
        end_time : str
            End time HH:MM

        """
        new_meal = pd.DataFrame(
            [
                {
                    "date": pd.to_datetime(date),
                    "start_time": str(pd.to_datetime(start_time).time()),
                    "end_time": str(pd.to_datetime(end_time).time()),
                }
            ]
        )
        # To compute all columns, we also need the previous meal
        new_entry = self.compute_columns(
            pd.concat([self.df.iloc[[-1]][self.base_fields], new_meal])
        ).iloc[[-1]]
        # Merging and saving to file
        self.df = pd.concat([self.df, new_entry])

    def delete_latest(self) -> None:
        """Delete latest meal from dataset."""
        self.df = self.df.drop(self.df.tail(1).index)

    def save_to_file(self) -> None:
        """Save data back to excel file."""
        self.df[self.base_fields].to_excel(self.file_path, index=False)
