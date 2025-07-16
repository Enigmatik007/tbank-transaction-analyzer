from src.utils.helpers import normalize_card_number


def test_normalize_card_number():
    assert normalize_card_number("*1234") == "*1234"
    assert normalize_card_number("5678") == "*5678"
    assert normalize_card_number("") == ""
    assert normalize_card_number(None) == ""
    assert normalize_card_number(1234) == ""
