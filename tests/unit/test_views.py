# tests/unit/test_views.py
import pytest
from datetime import datetime
from src.core.web.views import home_page

def test_home_page_valid_date():
    result = home_page("2023-01-01 12:00:00")
    assert "Добро пожаловать! 01 January 2023" in result["greeting"]
    assert isinstance(result["currency_rates"]["USD"], float)

def test_home_page_invalid_date():
    with pytest.raises(ValueError):
        home_page("invalid-date-format")
