"""Тесты для модуля services.py."""

import pytest

from src.core.services.services import investment_bank, profitable_cashback_categories


@pytest.fixture
def cashback_data():
    """Фикстура для тестирования кешбэка."""
    return [
        {"Дата операции": "2023-01-01", "Категория": "Супермаркеты", "Сумма операции": -1000, "Кэшбэк": 10},
        {"Дата операции": "2023-01-02", "Категория": "АЗС", "Сумма операции": -500, "Кэшбэк": 5},
    ]


def test_profitable_cashback_categories(cashback_data):
    """Тест анализа выгодных категорий."""
    result = profitable_cashback_categories(cashback_data, 2023, 1)
    assert result == {"Супермаркеты": 10.0, "АЗС": 5.0}


def test_investment_bank():
    """Тест расчета инвесткопилки."""
    transactions = [
        {"Дата операции": "2023-01-01", "Сумма операции": 123},
        {"Дата операции": "2023-01-02", "Сумма операции": 178},
    ]
    result = investment_bank("2023-01", transactions, 50)
    # (150 - 123) + (200 - 178) = 27 + 22 = 49
    assert result == 49.0


def test_investment_bank_empty():
    """Тест на случай отсутствия транзакций за месяц."""
    result = investment_bank("2023-02", [], 50)
    assert result == 0.0
