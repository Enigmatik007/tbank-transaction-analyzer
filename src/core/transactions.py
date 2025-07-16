from typing import Tuple

import pandas as pd


def load_transactions(path: str = "data/raw/operations.xlsx") -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    # Автоматическое распознавание с dayfirst=True для российского формата,
    # но при этом не задаём format, чтобы не ломать разные варианты дат
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="raise")
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True, errors="raise")

    return df


def filter_by_date(df: pd.DataFrame, date_range: Tuple[str, str]) -> pd.DataFrame:
    """Фильтрует транзакции по диапазону дат."""
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    return df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
