from unittest.mock import Mock 
from getdate_testing import get_date
import pytest

def test_getdate(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2022-10-33")
    with pytest.raises(ValueError):
        get_date()