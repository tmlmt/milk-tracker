from pathlib import Path

import pytest
from models.memories import MemoriesDataModel
from schemas.memory import Memory

fixture_file_path = Path(__file__).parent.resolve() / "fixtures" / "memory_sample.csv"


@pytest.fixture()
def m() -> MemoriesDataModel:
    """Return initial model to be used for testing."""
    return MemoriesDataModel(fixture_file_path)


def test_init_memories(m: MemoriesDataModel, snapshot: list) -> None:
    """Test constructor."""
    assert m.df.to_dict() == snapshot


def test_add_row(m: MemoriesDataModel, snapshot: list) -> None:
    """Test add_row()."""
    new_m = Memory(date="2024-02-15", description="A new memory")
    m.add(new_m)
    assert m.df.to_dict() == snapshot
