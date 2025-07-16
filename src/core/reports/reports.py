# src/core/reports/reports.py

import pandas as pd
from collections import defaultdict

def generate_spending_report(df: pd.DataFrame) -> dict:
    """Формирует отчёт по тратам за 3 последних месяца по категориям."""
    df = df.copy()
    df["Месяц"] = df["Дата операции"].dt.to_period("M")
    last_3_months = df["Месяц"].sort_values().unique()[-3:]

    report = defaultdict(float)
    for month in last_3_months:
        month_df = df[df["Месяц"] == month]
        grouped = month_df.groupby("Категория")["Сумма операции"].sum()
        for category, value in grouped.items():
            report[str(month), category] += abs(value)

    return dict(report)

