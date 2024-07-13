import datetime
from pathlib import Path

import pytest
from inline_snapshot import snapshot
from models.memories import MemoriesDataModel
from schemas.memory import Memory

fixture_file_path = Path(__file__).parent.resolve() / "fixtures" / "memory_sample.csv"


@pytest.fixture()
def m() -> MemoriesDataModel:
    """Return initial model to be used for testing."""
    return MemoriesDataModel(fixture_file_path)


def test_init_memories(m: MemoriesDataModel) -> None:
    """Test constructor."""
    assert m.df.to_dict("records") == snapshot(
        [
            {
                "date": datetime.date(2024, 3, 1),
                "description": "Yes, it did",
                "index": 0,
            },
            {
                "date": datetime.date(2024, 2, 1),
                "description": "I can't believe it happened!",
                "index": 1,
            },
        ]
    )


def test_add_row(m: MemoriesDataModel) -> None:
    """Test add_row()."""
    new_m = Memory(date="2024-02-15", description="A new memory")
    m.add(new_m)
    assert m.df.to_dict("records") == snapshot(
        [
            {
                "date": datetime.date(2024, 3, 1),
                "description": "Yes, it did",
                "index": 0,
            },
            {
                "date": datetime.date(2024, 2, 15),
                "description": "A new memory",
                "index": 1,
            },
            {
                "date": datetime.date(2024, 2, 1),
                "description": "I can't believe it happened!",
                "index": 2,
            },
        ]
    )


def test_remove_row(m: MemoriesDataModel) -> None:
    """Test remove_row()."""
    m.remove(0)
    assert m.df.to_dict("records") == snapshot(
        [
            {
                "date": datetime.date(2024, 2, 1),
                "description": "I can't believe it happened!",
                "index": 0,
            }
        ]
    )


def test_edit_row(m: MemoriesDataModel) -> None:
    """Test edit_row()."""
    edited_m = Memory(date="2024-02-15", description="Edited memory")
    m.edit(0, edited_m)
    assert m.df.to_dict("records") == snapshot(
        [
            {
                "date": datetime.date(2024, 2, 15),
                "description": "Edited memory",
                "index": 0,
            },
            {
                "date": datetime.date(2024, 2, 1),
                "description": "I can't believe it happened!",
                "index": 1,
            },
        ]
    )
