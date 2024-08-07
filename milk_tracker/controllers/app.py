import os
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import yaml
from dotenv import load_dotenv
from models.meals import MealsDataModel
from models.memories import MemoriesDataModel
from nicegui import app
from pydantic import ValidationError
from schemas.computed import ComputedValues
from schemas.config import Config
from schemas.meal import FinishedMeal, OngoingMeal
from utils.time_utils import get_current_date, get_current_time, is_today, time_since


class AppController:
    """Controls config, data and computed values."""

    def __init__(self, config_file: Path) -> None:  # noqa: D107
        # Load configuration
        self.config: Config = self.load_config_from_yaml(config_file)
        # Load environment variables
        load_dotenv()
        self.env = os.environ
        # Initialize computed values
        self.computed: ComputedValues = ComputedValues()
        # Initialize some state values
        self._ongoing_meal: Union[OngoingMeal, None] = None
        if app.storage.general.get("ongoing_meal", None):
            self._ongoing_meal = OngoingMeal(
                **app.storage.general.get("ongoing_meal", None)
            )
        self.latest_date_vitamins_baby = app.storage.general.get(
            "latest_date_vitamins_baby", None
        )
        self.latest_date_vitamins_mother = app.storage.general.get(
            "latest_date_vitamins_mother", None
        )
        self.compute_has_baby_taken_vitamins_today()
        self.compute_has_mother_taken_vitamins_today()

    # Properties getters and setters

    @property
    def ongoing_meal(self) -> Union[OngoingMeal, None]:
        """Ongoing meal."""
        return self._ongoing_meal

    @ongoing_meal.setter
    def ongoing_meal(self, value: OngoingMeal) -> None:
        self._ongoing_meal = value
        self.save_ongoing_meal()

    # Loading / Configuration

    def load_meals(self) -> None:
        """Load meal data and datamodel."""
        self.meals = MealsDataModel(
            Path(self.config.ASSETS_DIR) / self.config.MEALS_FILE_NAME
        )
        # Add ongoing_meal if it was loaded from storage
        if self.ongoing_meal:
            self.meals.add(self.ongoing_meal)
        self.do_continuous_update(force_all=True)
        self.compute_latest_meal_info()
        self.compute_is_ongoing_meal()

    def load_config_from_yaml(self, file_path: Path) -> Config:
        """Load configuration from the default yaml file.

        Parameters
        ----------
        file_path : Path
            path of the yaml file to load

        Returns
        -------
        dict
            configuration

        """
        try:
            with open(file_path) as file:
                config_dict = yaml.safe_load(file)
            config = Config(**config_dict)
        except FileNotFoundError:
            # TODO(tmlmt): Introduce logger
            # https://github.com/tmlmt/milk-tracker/issues/23
            print(f"Error: The file {file_path} does not exist.")
            raise
        except yaml.YAMLError:
            print(f"Error: The file {file_path} is not a valid YAML.")
            raise
        except ValidationError as e:
            print(f"Configuration is invalid: {e}")
            raise
        else:
            return config

    def load_memories(self) -> None:
        """Load memories and handler."""
        self.memories = MemoriesDataModel(
            file_path=Path(self.config.ASSETS_DIR) / self.config.MEMORIES_FILE_NAME,
            birthday=self.config.BIRTHDAY,
        )

    # Computes

    def compute_time_since_latest_end(self) -> None:
        """Update computed value "time_since_latest_end"."""
        # If a meal is ongoing, the counter is fixed and shows the
        # difference between the start of that meal and the end of
        # previous finished meal
        if self.ongoing_meal:
            self.computed.time_since_latest_end = (
                self.ongoing_meal.get_start_datetime()
                - self.meals.df[self.meals.df["end_time"] != ""].iloc[-1]["end_datetime"]
            )
        # Otherwise, we continuously show the difference between
        # the current time and the start of the previous finished meal
        # which is on the last row
        else:
            self.computed.time_since_latest_end = (
                pd.Timestamp.now() - self.meals.df.iloc[-1]["end_datetime"]
            )

    def compute_time_since_latest_start(self) -> None:
        """Update computed value "time_since_latest_start"."""
        # If a meal is ongoing, the counter is fixed and shows the
        # difference between the start of that meal and the start of
        # previous finished meal
        if self.ongoing_meal:
            self.computed.time_since_latest_start = (
                self.ongoing_meal.get_start_datetime()
                - self.meals.df[self.meals.df["end_time"] != ""].iloc[-1][
                    "start_datetime"
                ]
            )
        # Otherwise, we continuously show the difference between
        # the current time and the start of previous finished meal
        # which is on the last row
        else:
            self.computed.time_since_latest_start = (
                pd.Timestamp.now() - self.meals.df.iloc[-1]["start_datetime"]
            )

    def compute_latest_meal_info(self) -> None:
        """Update computed value "time_since_latest_start"."""
        latest_finished_meal = self.meals.df[self.meals.df["end_time"] != ""].iloc[-1]
        self.computed.latest_meal_info = f"""\
        Date: {latest_finished_meal["date"].date()}<br />
        Start time: {latest_finished_meal["start_time"]}<br />
        End time: {latest_finished_meal["end_time"]}<br />
        Duration: {latest_finished_meal["duration_hrmin"]}
        """

    def compute_current_time(self) -> None:
        """Update computed value "current_time"."""
        self.computed.current_time = get_current_time(include_sec=True)

    def compute_timer_meal_round(self) -> None:
        """Update timer for meal round."""
        # Look for the active round
        if not self.ongoing_meal:
            return
        active_round = next((r for r in self.ongoing_meal.rounds if r.is_active), None)
        if active_round:
            self.computed.timer_meal_round = time_since(active_round.start_datetime)
        else:
            self.computed.timer_meal_round = "00:00"

    def compute_is_ongoing_meal(self) -> None:
        """Update lock state of input field for start_time."""
        self.computed.is_ongoing_meal = bool(self.ongoing_meal)
        self.computed.is_ongoing_meal_paused = bool(
            self.ongoing_meal and not any(r.is_active for r in self.ongoing_meal.rounds)
        )
        self.computed.is_ongoing_meal_buttontxt = (
            "New round" if self.computed.is_ongoing_meal_paused else "Pause"
        )

    def compute_has_baby_taken_vitamins_today(self) -> None:
        """Boolean for whether baby has taken vitamins today."""
        if self.latest_date_vitamins_baby and is_today(self.latest_date_vitamins_baby):
            self.computed.has_baby_taken_vitamins_today = True
        else:
            self.computed.has_baby_taken_vitamins_today = False

    def compute_has_mother_taken_vitamins_today(self) -> None:
        """Boolean for whether mother has taken vitamins today."""
        if self.latest_date_vitamins_mother and is_today(
            self.latest_date_vitamins_mother
        ):
            self.computed.has_mother_taken_vitamins_today = True
        else:
            self.computed.has_mother_taken_vitamins_today = False

    def compute_all_meal(self) -> None:
        """Compute all computes except current time."""
        self.compute_is_ongoing_meal()
        self.compute_latest_meal_info()
        self.compute_time_since_latest_end()
        self.compute_time_since_latest_start()
        self.compute_timer_meal_round()

    # Getters

    def get_input_default_value_newmeal_start_time(self) -> str:
        """View: determine default value for input field start time new meal."""
        if self.ongoing_meal:
            return self.ongoing_meal.start_time
        return get_current_time(include_sec=False)

    # Actions

    def start_new_meal(
        self,
        date: Optional[str] = get_current_date(),
        start_time: Optional[str] = get_current_time(include_sec=False),
    ) -> None:
        """Start a new meal with default value (i.e. start now).

        Add to dataset
        """
        self.ongoing_meal = OngoingMeal(date=date, start_time=start_time)
        self.meals.add(self.ongoing_meal)
        self.compute_all_meal()

    def save_ongoing_meal(self) -> None:
        """Save ongoing meal to General Storage."""
        if self.ongoing_meal:
            # Can only store serializable values
            app.storage.general.update({"ongoing_meal": self.ongoing_meal.model_dump()})
        else:
            app.storage.general.update({"ongoing_meal": None})

    def cancel_ongoing_meal(self) -> None:
        """Remove ongoing meal from state and dataset."""
        self.meals.delete_latest("ongoing")
        self.ongoing_meal = None
        self.compute_all_meal()

    def add_finished_meal(self, date: str, start_time: str, end_time: str) -> None:
        """Add finished meal to dataset and update computed values."""
        meal = FinishedMeal(date=date, start_time=start_time, end_time=end_time)
        self.meals.add(meal)
        self.meals.save_to_file()
        self.compute_all_meal()

    def delete_latest_meal(self) -> None:
        """Delete latest meal from dataset and update computed values."""
        self.meals.delete_latest()
        # If there's an ongoing meal, we're just removing it from the live table
        if not self.ongoing_meal:
            self.meals.save_to_file()
        self.compute_all_meal()

    def pause_current_meal_round(self) -> None:
        """Pause current meal round now."""
        if self.ongoing_meal:
            self.ongoing_meal.pause()
            self.compute_is_ongoing_meal()
            self.compute_timer_meal_round()

    def start_new_meal_round(self) -> None:
        """Start new meal round now."""
        if self.ongoing_meal:
            self.ongoing_meal.start_new_round()
            self.compute_is_ongoing_meal()

    def confirm_vitamins_baby(self) -> None:
        """Update latest date baby has taken vitamins to today's date."""
        self.latest_date_vitamins_baby = get_current_date()
        app.storage.general.update(
            {"latest_date_vitamins_baby": self.latest_date_vitamins_baby}
        )
        self.compute_has_baby_taken_vitamins_today()

    def confirm_vitamins_mother(self) -> None:
        """Update latest date mother has taken vitamins to today's date."""
        self.latest_date_vitamins_mother = get_current_date()
        app.storage.general.update(
            {"latest_date_vitamins_mother": self.latest_date_vitamins_mother}
        )
        self.compute_has_mother_taken_vitamins_today()

    def do_continuous_update(self, *, force_all: bool = False) -> None:
        """Continuous update of computed values."""
        self.compute_current_time()
        self.compute_timer_meal_round()
        if self.computed.current_time[-2:] == "00" or force_all:
            self.compute_time_since_latest_end()
            self.compute_time_since_latest_start()
            self.compute_has_baby_taken_vitamins_today()
            self.compute_has_mother_taken_vitamins_today()
