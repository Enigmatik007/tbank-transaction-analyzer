# tests/unit/test_transactions.py

import pandas as pd

from src.core.transactions import load_transactions


def test_load_transactions(tmp_path):
    # Создаем временный Excel-файл
    file = tmp_path / "operations.xlsx"
    df = pd.DataFrame(
        {
            "Дата операции": ["2021-12-31 16:44:00"],
            "Дата платежа": ["2021-12-31"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма операции": [-160.89],
            "Валюта операции": ["RUB"],
            "Сумма платежа": [-160.89],
            "Валюта платежа": ["RUB"],
            "Кэшбэк": [""],
            "Категория": ["Супермаркеты"],
            "MCC": [5411],
            "Описание": ["Колхоз"],
            "Бонусы (включая кэшбэк)": [3.00],
            "Округление на инвесткопилку": [0.00],
            "Сумма операции с округлением": [160.89],
        }
    )
    df.to_excel(file, index=False)

    result = load_transactions(str(file))
    assert not result.empty
    assert "Дата операции" in result.columns
