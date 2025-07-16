# src/core/web/views.py
from datetime import datetime
from typing import Dict, List
import pandas as pd
from src.api.finance_client import FinanceClient


def home_page(datetime_str: str) -> Dict:
    """
    Генерирует JSON для главной страницы согласно ТЗ.

    Args:
        datetime_str: Дата в формате 'YYYY-MM-DD HH:MM:SS'

    Returns:
        {
            "greeting": str,
            "cards": List[Dict],
            "top_transactions": List[Dict],
            "currency_rates": Dict[str, float]
        }

    Пример вызова:
    >>> home_page("2023-01-01 12:00:00")
    {
        "greeting": "Добро пожаловать! 01 January 2023",
        "cards": [{"id": 1, "balance": 15000.50}],
        "top_transactions": [
            {"amount": 5000, "category": "shopping"},
            {"amount": 3000, "category": "food"}
        ],
        "currency_rates": {"USD": 75.45, "EUR": 90.20}
    }
    """
    # Парсим дату
    try:
        date_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        raise ValueError(f"Неверный формат даты. Ожидается 'YYYY-MM-DD HH:MM:SS'. Ошибка: {str(e)}")

    # Получаем курсы валют
    client = FinanceClient()
    currency_rates = {
        "USD": client.get_currency_rate("USD"),
        "EUR": client.get_currency_rate("EUR")
    }

    # Формируем ответ
    return {
        "greeting": f"Добро пожаловать! {date_obj.strftime('%d %B %Y')}",
        "cards": _get_user_cards(),  # Вспомогательная функция
        "top_transactions": _get_top_transactions(),
        "currency_rates": currency_rates
    }


def _get_user_cards() -> List[Dict]:
    """Возвращает список карт пользователя (заглушка)"""
    return [{"id": 1, "balance": 15000.50}]


def _get_top_transactions() -> List[Dict]:
    """Возвращает топ-5 транзакций (заглушка)"""
    return [
        {"amount": 5000, "category": "shopping"},
        {"amount": 3000, "category": "food"}
    ]
