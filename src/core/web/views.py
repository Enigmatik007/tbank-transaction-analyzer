"""Модуль представлений для веб-страниц."""

from datetime import datetime
import logging
from typing import Any, Dict, List

import pandas as pd

from src.api.finance_client import get_currency_rates, get_stock_prices
from src.core.transactions import filter_by_date, load_transactions

logger = logging.getLogger(__name__)


def home_page(datetime_str: str) -> Dict[str, Any]:
    """
    Генерирует данные для главной страницы.

    Args:
        datetime_str: Дата и время в формате 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        Dict[str, Any]: JSON-ответ для страницы.
    """
    try:
        dt = datetime.fromisoformat(datetime_str)

        # Приветствие
        greeting = _get_greeting(dt.hour)

        # Загрузка и фильтрация данных
        df = load_transactions()
        df = filter_by_date(df, (dt.replace(day=1).strftime("%Y-%m-%d"), datetime_str))

        return {
            "greeting": greeting,
            "cards": _calculate_cards_stats(df),
            "top_transactions": _get_top_transactions(df),
            "currency_rates": get_currency_rates(),
            "stock_prices": get_stock_prices(),
        }

    except Exception as e:
        logger.error(f"Error in home_page: {str(e)}")
        return {"error": str(e)}


def _get_greeting(hour: int) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def _calculate_cards_stats(df: pd.DataFrame) -> List[Dict[str, float]]:
    """Рассчитывает статистику по картам."""
    cards = []
    for card in df["Номер карты"].unique():
        card_df = df[df["Номер карты"] == card]
        total_spent = card_df[card_df["Сумма операции"] < 0]["Сумма операции"].sum() * -1
        cards.append(
            {"last_digits": card[-4:], "total_spent": round(total_spent, 2), "cashback": round(total_spent * 0.01, 2)}
        )
    return cards


def _get_top_transactions(df: pd.DataFrame, n: int = 5) -> List[Dict[str, str]]:
    """
    Возвращает топ-N транзакций по сумме.

    Args:
        df (pd.DataFrame): Таблица транзакций.
        n (int): Количество транзакций в топе. По умолчанию 5.

    Returns:
        List[Dict[str, str]]: Список словарей с данными по транзакциям.
    """
    records: List[Dict[str, str]] = (
        df.nlargest(n, "Сумма операции")[["Дата операции", "Сумма операции", "Категория", "Описание"]]
        .astype(str)
        .to_dict("records")
    )
    return records
