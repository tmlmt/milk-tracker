from pathlib import Path

from schemas.config import Config

fixture_dir_path = Path(__file__).parent.resolve() / ".." / "assets"


def test_default_config() -> None:
    """Test the default config.

    Must be run from parent directory of the tests folder
    """
    _ = Config(
        TITLE="Milk Tracker",
        MAX_PASSWORD_ATTEMPTS=3,
        ASSETS_DIR=fixture_dir_path,
        MEALS_FILE_NAME="journal.xlsx",
        MEMORIES_FILE_NAME="memories.csv",
        PLOTLY_DEFAULT_CONFIG={
            "modeBarButtonsToRemove": [
                "zoom2d",
                "pan2d",
                "select2d",
                "lasso2d",
                "zoomIn2d",
                "zoomOut2d",
            ]
        },
        BIRTHDAY="2024-02-01",
    )
