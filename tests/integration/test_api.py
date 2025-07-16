# tests/integration/test_api.py

from src.api.finance_client import get_currency_rates


def test_currency_rates_format():
    rates = get_currency_rates()
    assert "USD_RUB" in rates
    assert "EUR_RUB" in rates
    assert isinstance(rates["USD_RUB"], float)
