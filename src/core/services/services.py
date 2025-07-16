# src/core/services/services.py

import pandas as pd

def calculate_cashback(df: pd.DataFrame) -> float:
    """Рассчитывает суммарный кешбэк (1% от всех расходов RUB)."""
    rub_expenses = df[(df["Валюта операции"] == "RUB") & (df["Сумма операции"] < 0)]
    cashback = -rub_expenses["Сумма операции"].sum() * 0.01
    return round(cashback, 2)

def round_transactions(df: pd.DataFrame, step: int = 10) -> pd.DataFrame:
    """Округляет суммы операций и сохраняет разницу в 'Округление на инвесткопилку'."""
    df = df.copy()
    def calc_round(row):
        if row["Сумма операции"] < 0:
            amount = abs(row["Сумма операции"])
            remainder = step - (amount % step)
            return 0 if remainder == step else round(remainder, 2)
        return 0

    df["Округление на инвесткопилку"] = df.apply(calc_round, axis=1)
    df["Сумма операции с округлением"] = abs(df["Сумма операции"]) + df["Округление на инвесткопилку"]
    return df
