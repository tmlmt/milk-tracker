from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, DirectoryPath, Field, field_validator, model_validator
from typing_extensions import Self


class Config(BaseModel):
    """Configuration Model."""

    ASSETS_DIR: DirectoryPath = Field(..., description="Directory path for assets")
    DATA_FILE_NAME: Path = Field(..., description="Journal file in Excel format")
    PLOTLY_DEFAULT_CONFIG: Dict[str, Any] = Field(
        ..., description="Default config value for Plotly plots"
    )

    @field_validator("DATA_FILE_NAME")
    @classmethod
    def check_file_extension(cls, v: Path) -> Path:  # noqa: D102
        if v.suffix != ".xlsx":
            msg = "FILE_NAME must have an .xlsx extension"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def file_exists(self) -> Self:  # noqa: D102
        full_path = Path(self.ASSETS_DIR) / self.DATA_FILE_NAME
        if not full_path.is_file():
            msg = f"{full_path} does not exist"
            raise ValueError(msg)
        return self
