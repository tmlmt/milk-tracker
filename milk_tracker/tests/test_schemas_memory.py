from datetime import date, datetime

import numpy as np
import pytest
import time_machine
from pydantic import ValidationError
from schemas.memory import Memory
from zoneinfo import ZoneInfo


@time_machine.travel(datetime(2024, 6, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen")))
def test_default_memory() -> None:
    """Test default Memory constructor."""
    m = Memory()
    assert m.date_field == date.today()
    assert m.description == "-"


def test_empty_description() -> None:
    """Description cannot be empty."""
    with pytest.raises(ValidationError):
        _ = Memory(description="")


@time_machine.travel(datetime(2024, 6, 10, 20, 50, tzinfo=ZoneInfo("Europe/Copenhagen")))
def test_constructor_memory() -> None:
    """Test other ways to initialize a Memory."""
    # Using the date alias
    m = Memory(date="2024-01-02")
    assert m.date_field == date(2024, 1, 2)
    # Using the initial date field name should lead to it not being used
    m = Memory(date_field="2024-01-02")
    assert m.date_field == date(2024, 6, 10)
    # Using an actual date
    m = Memory(date=date(2024, 5, 6))
    assert m.date_field == date(2024, 5, 6)
    # With a description
    desc = "My description"
    m = Memory(description=desc)
    assert m.description == desc


def test_to_dataframe() -> None:
    """Test conversion to dataframe."""
    m = Memory(date="2024-01-02", description="My description")
    df_test = m.to_dataframe()
    assert len(df_test) == 1
    assert df_test.loc[0, "description"] == "My description"
    assert df_test.loc[0, "date"] == date(2024, 1, 2)
    assert df_test.dtypes["date"] == np.dtype(
        "O"
    )  # Python object, source: https://stackoverflow.com/a/37562101/4258693


def test_to_dict() -> None:
    """Test conversion to dictionnary."""
    m = Memory(date="2024-01-02", description="My description")
    m_dict = m.to_dict()
    assert (m_dict) == {"date": date(2024, 1, 2), "description": "My description"}
