# tests/unit/test_services.py

import pandas as pd

from src.core.services.services import calculate_cashback, round_transactions


def test_calculate_cashback():
    data = {
        "Сумма операции": [-100.0, -200.0, -300.0, 500.0],
        "Валюта операции": ["RUB", "RUB", "USD", "RUB"],
    }
    df = pd.DataFrame(data)
    result = calculate_cashback(df)
    # Кешбэк должен считаться только от отрицательных RUB операций: -100, -200 = 1% от 300 = 3.0
    assert result == 3.0


def test_round_transactions():
    data = {
        "Сумма операции": [-158.20, -41.80, 0.0],
    }
    df = pd.DataFrame(data)
    result = round_transactions(df, step=10)

    expected_roundings = [1.80, 8.20, 0.0]
    expected_total = [160.0, 50.0, 0.0]

    assert list(result["Округление на инвесткопилку"]) == expected_roundings
    assert list(result["Сумма операции с округлением"]) == expected_total
