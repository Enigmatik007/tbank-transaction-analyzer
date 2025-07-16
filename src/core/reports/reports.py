"""Модуль для генерации отчетов по транзакциям."""

from datetime import datetime
import logging
from typing import Dict, Optional, cast

import pandas as pd

logger = logging.getLogger(__name__)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, float]:
    """
    Возвращает траты по категории за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями.
        category: Название категории для анализа.
        date: Опциональная дата в формате 'YYYY-MM-DD'.
              Если не указана, используется текущая дата.

    Returns:
        Dict[str, float]: Словарь с месяцами и суммами.
    """
    try:
        parsed_date = pd.to_datetime(date) if date else datetime.now()
        start_date = parsed_date - pd.DateOffset(months=3)

        filtered = transactions[
            (transactions["Категория"] == category)
            & (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= parsed_date)
        ]

        grouped = (
            filtered.groupby(filtered["Дата операции"].dt.to_period("M"))["Сумма операции"]
            .sum()
            .apply(lambda x: round(float(x), 2))
        )

        logger.info(f"Generated spending report for category: {category}")
        return cast(Dict[str, float], {str(k): v for k, v in grouped.to_dict().items()})

    except Exception as e:
        logger.error(f"Error in spending_by_category: {str(e)}")
        raise


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    """
    Возвращает средние траты по дням недели за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями.
        date: Опциональная дата в формате 'YYYY-MM-DD'.

    Returns:
        Dict[str, float]: Словарь с днями недели и средними тратами.
    """
    try:
        parsed_date = pd.to_datetime(date) if date else datetime.now()
        start_date = parsed_date - pd.DateOffset(months=3)

        filtered = transactions[
            (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= parsed_date)
        ]

        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        grouped = (
            filtered.groupby(filtered["Дата операции"].dt.weekday)["Сумма операции"]
            .mean()
            .round(2)
            .rename(index=dict(enumerate(weekdays)))
        )

        logger.info("Generated weekday spending report")
        return cast(Dict[str, float], grouped.to_dict())

    except Exception as e:
        logger.error(f"Error in spending_by_weekday: {str(e)}")
        raise


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    """
    Возвращает средние траты в рабочие/выходные дни за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями.
        date: Опциональная дата в формате 'YYYY-MM-DD'.

    Returns:
        Dict[str, float]: Словарь с ключами 'workday' и 'weekend'.
    """
    try:
        parsed_date = pd.to_datetime(date) if date else datetime.now()
        start_date = parsed_date - pd.DateOffset(months=3)

        filtered = transactions[
            (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= parsed_date)
        ].copy()

        filtered["is_weekend"] = filtered["Дата операции"].dt.weekday >= 5
        grouped = (
            filtered.groupby("is_weekend")["Сумма операции"]
            .mean()
            .round(2)
            .rename({False: "workday", True: "weekend"})
        )

        logger.info("Generated workday/weekend spending report")
        return cast(Dict[str, float], grouped.to_dict())

    except Exception as e:
        logger.error(f"Error in spending_by_workday: {str(e)}")
        raise
