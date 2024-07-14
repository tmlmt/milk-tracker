from datetime import date
from pathlib import Path
from typing import Any, Dict

from pydantic import (
    BaseModel,
    DirectoryPath,
    Field,
    PositiveInt,
    field_validator,
    model_validator,
)
from typing_extensions import Self


class Config(BaseModel):
    """Configuration Model."""

    ASSETS_DIR: DirectoryPath = Field(..., description="Directory path for assets")
    MEALS_FILE_NAME: Path = Field(..., description="Journal file in Excel format")
    MEMORIES_FILE_NAME: Path = Field(..., description="Memories file in CSV format")
    PLOTLY_DEFAULT_CONFIG: Dict[str, Any] = Field(
        ..., description="Default config value for Plotly plots"
    )
    TITLE: str = Field(
        ..., description="Title of the app as it appears in the browser tab"
    )
    MAX_PASSWORD_ATTEMPTS: PositiveInt
    BIRTHDAY: date = Field(..., description="Birthday date")

    @field_validator("MEALS_FILE_NAME")
    @classmethod
    def check_xlsx_file_extension(cls, v: Path) -> Path:  # noqa: D102
        if v.suffix != ".xlsx":
            msg = "FILE_NAME must have an .xlsx extension"
            raise ValueError(msg)
        return v

    @field_validator("MEMORIES_FILE_NAME")
    @classmethod
    def check_csv_file_extension(cls, v: Path) -> Path:  # noqa: D102
        if v.suffix != ".csv":
            msg = "FILE_NAME must have a. csv extension"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def file_exists(self) -> Self:  # noqa: D102
        full_path = Path(self.ASSETS_DIR) / self.MEALS_FILE_NAME
        if not full_path.is_file():
            msg = f"{full_path} does not exist"
            raise ValueError(msg)
        full_path = Path(self.ASSETS_DIR) / self.MEMORIES_FILE_NAME
        if not full_path.is_file():
            msg = f"{full_path} does not exist"
            raise ValueError(msg)
        return self
