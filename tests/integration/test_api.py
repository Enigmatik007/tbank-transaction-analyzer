# tests/integration/test_api.py

from src.api.finance_client import get_currency_rates


def test_currency_rates_format():
    rates = get_currency_rates()
    # Проверяем новый формат ответа
    assert any(item["currency"] == "USD" for item in rates)
    assert isinstance(rates[0]["rate"], float)
