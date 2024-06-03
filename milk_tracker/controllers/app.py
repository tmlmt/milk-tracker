import os
from pathlib import Path

import pandas as pd
import yaml
from dotenv import load_dotenv
from models.data import DataModel
from pydantic import ValidationError
from schemas.computed import ComputedValues
from schemas.config import Config
from utils.time_utils import get_current_time


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

    def load_data(self) -> None:
        """Load meal data and datamodel."""
        self.meals = DataModel(Path(self.config.ASSETS_DIR) / self.config.DATA_FILE_NAME)
        self.do_continuous_update(force_all=True)
        self.compute_latest_meal_info()

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

    def compute_time_since_latest_end(self) -> None:
        """Update computed value "time_since_latest_end"."""
        self.computed.time_since_latest_end = (
            pd.Timestamp.now() - self.meals.df.iloc[-1]["end_datetime"]
        )

    def compute_time_since_latest_start(self) -> None:
        """Update computed value "time_since_latest_start"."""
        self.computed.time_since_latest_start = (
            pd.Timestamp.now() - self.meals.df.iloc[-1]["start_datetime"]
        )

    def compute_latest_meal_info(self) -> None:
        """Update computed value "time_since_latest_start"."""
        self.computed.latest_meal_info = f"""\
        Date: {self.meals.df.iloc[-1]["date"].date()}<br />
        Start time: {self.meals.df.iloc[-1]["start_time"]}<br />
        End time: {self.meals.df.iloc[-1]["end_time"]}<br />
        Duration: {self.meals.df.iloc[-1]["duration_hrmin"]}
        """

    def compute_current_time(self) -> None:
        """Update computed value "current_time"."""
        self.computed.current_time = get_current_time(include_sec=True)

    def do_continuous_update(self, *, force_all: bool = False) -> None:
        """Continuous update of computed values."""
        self.compute_current_time()
        if self.computed.current_time[-2:] == "00" or force_all:
            self.compute_time_since_latest_end()
            self.compute_time_since_latest_start()
