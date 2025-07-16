"""Общие фикстуры для тестов."""

from datetime import datetime, timedelta
import logging

import pandas as pd
import pytest


@pytest.fixture(scope="session")
def test_logger():
    """Фикстура для логгера тестов."""
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger("tests")


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    dates = [datetime.now() - timedelta(days=i) for i in range(10)]
    return pd.DataFrame(
        {
            "Дата операции": dates,
            "Номер карты": ["*1234", "*5678"] * 5,
            "Сумма операции": [-100 * (i + 1) for i in range(10)],
            "Категория": ["Супермаркеты", "АЗС"] * 5,
            "Кэшбэк": [i * 0.5 for i in range(10)],
            "Описание": ["Покупка"] * 10,
            "MCC": [5411, 5542] * 5,
        }
    )


@pytest.fixture(params=[10, 50, 100])
def rounding_step(request):
    """Параметризованная фикстура для шага округления."""
    return request.param


@pytest.fixture
def mock_currency_rates(monkeypatch):
    """Фикстура для мокирования API курсов валют."""

    def mock_get_rates():
        return [{"currency": "USD", "rate": 75.5}]

    monkeypatch.setattr("src.api.finance_client.get_currency_rates", mock_get_rates)
