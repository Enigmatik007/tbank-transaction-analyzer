"""Тесты для модуля reports.py."""

from datetime import datetime, timedelta

import pandas as pd
import pytest

from src.core.reports.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.fixture
def report_data():
    """Фикстура с тестовыми данными для отчетов."""
    dates = pd.date_range(end=datetime.now(), periods=90, freq="D")
    return pd.DataFrame(
        {
            "Дата операции": dates,
            "Категория": ["Супермаркеты"] * 45 + ["АЗС"] * 30 + ["Кафе"] * 15,
            "Сумма операции": [-100] * 45 + [-200] * 30 + [-300] * 15,
            "is_weekend": [d.weekday() >= 5 for d in dates],
        }
    )


@pytest.mark.parametrize("category,expected_months", [("Супермаркеты", 3), ("АЗС", 2), ("Кафе", 1)])
def test_spending_by_category(report_data, category, expected_months):
    """Параметризованный тест для отчета по категориям."""
    result = spending_by_category(report_data, category)
    assert len(result) == expected_months
    assert all(v < 0 for v in result.values())


@pytest.mark.parametrize("date_offset,expected_days", [(0, 7), (30, 7)])  # Текущая дата  # Дата 30 дней назад
def test_spending_by_weekday(report_data, date_offset, expected_days):
    """Тест для отчета по дням недели с параметризацией даты."""
    test_date = (datetime.now() - timedelta(days=date_offset)).strftime("%Y-%m-%d")
    result = spending_by_weekday(report_data, test_date)
    assert len(result) == expected_days
    assert "Пн" in result


@pytest.mark.parametrize("weekend_spend_factor,expected_ratio", [(1.0, 1.0), (2.0, 2.0)])
def test_spending_by_workday(weekend_spend_factor, expected_ratio):
    """Тест для отчета по рабочим и выходным дням."""
    fixed_date = datetime(2025, 7, 14)

    data = pd.DataFrame(
        {
            "Дата операции": pd.date_range(end=fixed_date, periods=14),  # 2 недели
            "Сумма операции": [-100] * 14,
            "is_weekend": [d.weekday() >= 5 for d in pd.date_range(end=fixed_date, periods=14)],
        }
    )
    data.loc[data["is_weekend"], "Сумма операции"] *= weekend_spend_factor

    result = spending_by_workday(data, date=fixed_date.strftime("%Y-%m-%d"))
    actual_ratio = abs(result["weekend"] / result["workday"])
    assert round(actual_ratio, 1) == expected_ratio


# Тесты на покрытие исключений для повышения покрытия кода


def test_spending_by_category_raises():
    """Тест проверки исключения в spending_by_category."""
    df = pd.DataFrame({"Категория": ["Супермаркеты"]})
    with pytest.raises(Exception) as excinfo:
        spending_by_category(df, category="Супермаркеты", date="неверный_формат_даты")
    assert "unable to parse" in str(excinfo.value)


def test_spending_by_weekday_raises():
    """Тест проверки исключения в spending_by_weekday."""
    df = pd.DataFrame({"Дата операции": ["not a date"], "Сумма операции": [100]})
    with pytest.raises(Exception) as excinfo:
        spending_by_weekday(df, date="invalid_date")
    assert "unable to parse" in str(excinfo.value)


def test_spending_by_workday_raises():
    """Тест проверки исключения в spending_by_workday."""
    df = pd.DataFrame({"Дата операции": ["not a date"], "Сумма операции": [100]})
    with pytest.raises(Exception) as excinfo:
        spending_by_workday(df, date="invalid_date")
    assert "unable to parse" in str(excinfo.value)
