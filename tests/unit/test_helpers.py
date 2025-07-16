"""Тесты для модуля helpers.py."""

from src.utils.helpers import normalize_card_number


def test_normalize_card_number():
    """Тест нормализации номера карты."""
    assert normalize_card_number("1234567890123456") == "*3456"
    assert normalize_card_number("*3456") == "*3456"
    assert normalize_card_number("") == ""
    assert normalize_card_number(None) == ""
