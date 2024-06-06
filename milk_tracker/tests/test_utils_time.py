import pytest
from utils.time_utils import force_full_time, is_time_format


def test_valid_time() -> None:
    """Test that should all pass."""
    assert is_time_format("14:01")
    assert is_time_format("14:01", "short")
    assert is_time_format("14:00:01")
    assert is_time_format("14:00:01", "full")


def test_invalid_short_time() -> None:
    """Test that should fail with short format."""
    assert not is_time_format("14:0", "short")
    assert not is_time_format("14:000", "short")
    assert not is_time_format("14-00", "short")
    assert not is_time_format("25:01", "short")
    assert not is_time_format("14:70", "short")
    assert not is_time_format("     ", "short")
    assert not is_time_format("", "short")
    assert not is_time_format(" ", "short")


def test_invalid_full_time() -> None:
    """Test that should fail with full format."""
    assert not is_time_format("14:00", "full")
    assert not is_time_format("14:01:0", "full")
    assert not is_time_format("14:01:011", "full")
    assert not is_time_format("25:01:01", "full")
    assert not is_time_format("14:70:01", "full")
    assert not is_time_format("        ", "full")
    assert not is_time_format("", "full")
    assert not is_time_format(" ", "full")


def test_force_full_time() -> None:
    """Test force_full_time()."""
    assert force_full_time("17:41") == "17:41:00"
    assert force_full_time("17:01:01") == "17:01:01"
    with pytest.raises(TypeError):
        force_full_time("17:0")
    with pytest.raises(TypeError):
        force_full_time("17h01")
