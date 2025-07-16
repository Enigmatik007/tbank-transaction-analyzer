"""Модуль с бизнес-логикой сервисов."""

import logging
from typing import Any, Dict, List, cast

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def profitable_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """
    Анализирует выгодные категории для кешбэка.

    Args:
        data: Список транзакций.
        year: Год для анализа.
        month: Месяц для анализа.

    Returns:
        Dict[str, float]: Словарь {категория: сумма кешбэка}.
    """
    try:
        df = pd.DataFrame(data)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])

        # Фильтрация по дате
        mask = (df["Дата операции"].dt.year == year) & (df["Дата операции"].dt.month == month)
        filtered = df.loc[mask]

        # Расчет кешбэка (1% от расходов)
        cashback_series = (
            filtered[filtered["Сумма операции"] < 0].groupby("Категория")["Сумма операции"].sum().mul(-0.01).round(2)
        )

        result = cast(Dict[str, float], cashback_series.to_dict())

        logger.info(f"Cashback analysis completed for {month}/{year}")
        return result

    except Exception as e:
        logger.error(f"Error in cashback analysis: {str(e)}")
        raise


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму для инвесткопилки через округление.

    Args:
        month: Месяц в формате 'YYYY-MM'.
        transactions: Список транзакций.
        limit: Шаг округления (10, 50, 100).

    Returns:
        float: Сумма для инвесткопилки.
    """
    try:
        df = pd.DataFrame(transactions)
        if df.empty or "Дата операции" not in df.columns or "Сумма операции" not in df.columns:
            logger.info("Empty or invalid transactions data")
            return 0.0

        df["Дата операции"] = pd.to_datetime(df["Дата операции"])

        # Фильтрация по месяцу
        year_num, month_num = map(int, month.split("-"))
        mask = (df["Дата операции"].dt.year == year_num) & (df["Дата операции"].dt.month == month_num)
        filtered = df.loc[mask]

        if filtered.empty:
            logger.info("No transactions found for the given month.")
            return 0.0

        # Округление
        rounded = np.ceil(filtered["Сумма операции"] / limit) * limit
        savings = (rounded - filtered["Сумма операции"]).sum()

        logger.info(f"Calculated savings: {savings:.2f} for {month_num}/{year_num}")
        return float(savings)

    except Exception as e:
        logger.error(f"Error in investment calculation: {str(e)}")
        raise
