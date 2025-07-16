"""Модуль для загрузки и обработки транзакций."""

import logging
from typing import Tuple

import pandas as pd

logger = logging.getLogger(__name__)


def load_transactions(path: str = "data/raw/operations.xlsx") -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла.

    Args:
        path: Путь к файлу с транзакциями.

    Returns:
        pd.DataFrame: DataFrame с транзакциями.
    """
    try:
        df = pd.read_excel(path)
        df.columns = df.columns.str.strip()

        # Конвертация дат: если колонка есть, конвертируем
        date_cols = ["Дата операции", "Дата платежа"]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

        # Обработка пустых значений
        if "Номер карты" in df.columns:
            df["Номер карты"] = df["Номер карты"].fillna("N/A")

        logger.info(f"Loaded {len(df)} transactions from {path}")
        return df

    except Exception as e:
        logger.error(f"Error loading transactions: {str(e)}")
        raise


def filter_by_date(df: pd.DataFrame, date_range: Tuple[str, str]) -> pd.DataFrame:
    """
    Фильтрует транзакции по диапазону дат.

    Args:
        df: DataFrame с транзакциями.
        date_range: Кортеж (начальная дата, конечная дата) в формате строк 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame.
    """
    try:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

        # Обеспечить, что колонка 'Дата операции' имеет тип datetime
        if df["Дата операции"].dtype == "O":
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

        mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
        filtered = df.loc[mask]
        logger.debug(f"Filtered to {len(filtered)} transactions")
        return filtered
    except Exception as e:
        logger.error(f"Error filtering by date: {str(e)}")
        raise
