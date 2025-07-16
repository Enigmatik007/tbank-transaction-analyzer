from unittest.mock import patch

import pandas as pd

from src.core.web.views import home_page


@patch("src.core.web.views.load_transactions")
@patch("src.core.web.views.get_currency_rates")
@patch("src.core.web.views.get_stock_prices")
def test_home_page_success(mock_stocks, mock_rates, mock_transactions):
    """Тест успешного формирования главной страницы."""
    mock_transactions.return_value = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2023-01-01 10:00:00"]),  # Приводим к datetime!
            "Номер карты": ["*1234"],
            "Сумма операции": [-100],
            "Категория": ["Супермаркеты"],
            "Описание": ["Покупка"],
        }
    )

    mock_rates.return_value = [{"currency": "USD", "rate": 75.5}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}]

    result = home_page("2023-01-01 12:00:00")

    assert "greeting" in result
    assert result["greeting"] == "Добрый день"
    assert isinstance(result["cards"], list)
    assert len(result["cards"]) == 1
    assert result["cards"][0]["last_digits"] == "1234"
    assert result["cards"][0]["total_spent"] == 100.0
    assert "currency_rates" in result
    assert "stock_prices" in result
    assert result["currency_rates"][0]["currency"] == "USD"
    assert result["stock_prices"][0]["stock"] == "AAPL"


def test_home_page_invalid_date():
    """Тест обработки неверного формата даты."""
    result = home_page("invalid_date")
    assert "error" in result
    assert "Invalid isoformat string" in result["error"]
