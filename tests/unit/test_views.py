# tests/unit/test_views.py

from src.core.web.views import home_page


def test_home_page_basic():
    result = home_page("2021-12-31T12:00:00")
    assert "greeting" in result
    assert isinstance(result["top_transactions"], list)
    assert isinstance(result["currency_rates"], dict)
