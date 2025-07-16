"""Тесты для модуля transactions.py."""

import pandas as pd
import pytest

from src.core.transactions import filter_by_date, load_transactions


def test_load_transactions_success(tmp_path):
    """
    Тест успешной загрузки транзакций из Excel-файла.

    Создается временный Excel-файл с тестовыми данными,
    проверяется, что данные корректно загружаются и колонки присутствуют.
    """
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame(
        {
            "Дата операции": ["2023-01-01"],
            "Дата платежа": ["2023-01-02"],  # Добавлена колонка, чтобы не падало
            "Номер карты": ["*1234"],
            "Сумма операции": [-100],
        }
    )
    df.to_excel(test_file, index=False)

    result = load_transactions(str(test_file))
    assert not result.empty
    assert "Дата операции" in result.columns
    assert "Дата платежа" in result.columns  # Проверяем новую колонку


def test_load_transactions_invalid_path():
    """
    Тест обработки ситуации с неверным путем к файлу.

    Ожидается вызов исключения FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError):
        load_transactions("invalid_path.xlsx")


def test_filter_by_date():
    """
    Тест фильтрации транзакций по диапазону дат.

    Создается DataFrame с двумя датами, фильтруется по одному месяцу,
    проверяется, что возвращается правильное количество строк.
    """
    df = pd.DataFrame({"Дата операции": pd.to_datetime(["2023-01-01", "2023-02-01"]), "Сумма операции": [-100, -200]})
    result = filter_by_date(df, ("2023-01-01", "2023-01-31"))
    assert len(result) == 1
    assert result.iloc[0]["Сумма операции"] == -100
