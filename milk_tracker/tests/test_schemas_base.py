from typing import Self

import pytest
from pydantic import ValidationError, model_validator
from schemas.base import UpdatableBaseModel


def test_simple_update() -> None:
    """Test simple update."""

    class Example(UpdatableBaseModel):
        a: int
        b: str

    # Initiate model
    e = Example(a=1, b="Yo")
    assert e.a == 1
    assert e.b == "Yo"

    # Update 1 field with update()
    new_value_a = 2
    e.update(a=new_value_a)
    assert e.a == new_value_a
    assert e.b == "Yo"

    # Update 1 field directly
    new_value_a = 3
    e.a = new_value_a
    assert e.a == new_value_a
    assert e.b == "Yo"

    # Update 2 fields
    new_value_a = 4
    new_value_b = "Yeah"
    e.update(a=new_value_a, b=new_value_b)
    assert e.a == new_value_a
    assert e.b == new_value_b


def test_delay_validation() -> None:
    """Test with model with model_validator."""

    class Example(UpdatableBaseModel):
        a: int
        b: int

        @model_validator(mode="after")
        def enforce_equal(self) -> Self:
            if self.a != self.b:
                msg = "a and b must be equal"
                raise ValueError(msg)
            return self

    # Initiate model
    e = Example(a=1, b=1)

    # This should not work
    with pytest.raises(ValidationError):
        e.a = 2
    with pytest.raises(ValidationError):
        e.update(a=2, b=3)
    # But this should work
    e.update(a=4, b=4)
    assert (e.a, e.b) == (4, 4)
    with e.delay_validation():
        e.a = 5
        e.b = 5
    assert (e.a, e.b) == (5, 5)
