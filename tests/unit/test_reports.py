# tests/unit/test_reports.py

import pandas as pd

from src.core.reports.reports import generate_spending_report


def test_generate_spending_report():
    data = {
        "Дата операции": pd.to_datetime(["2021-10-15", "2021-10-20", "2021-11-01", "2021-12-05"]),
        "Категория": ["Супермаркеты", "Супермаркеты", "Аптеки", "Аптеки"],
        "Сумма операции": [-100.0, -200.0, -300.0, -400.0],
    }
    df = pd.DataFrame(data)

    result = generate_spending_report(df)

    # Проверка, что ключи содержат нужные периоды и категории
    assert ("2021-10", "Супермаркеты") in result
    assert result[("2021-10", "Супермаркеты")] == 300.0
    assert result[("2021-11", "Аптеки")] == 300.0
    assert result[("2021-12", "Аптеки")] == 400.0
