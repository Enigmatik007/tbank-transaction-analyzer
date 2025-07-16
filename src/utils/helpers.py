def normalize_card_number(card: str) -> str:
    """
    Нормализует номер карты (оставляет последние 4 цифры и *).
    Пример: *1234
    """
    if not isinstance(card, str):
        return ""
    card = card.strip()
    if card.startswith("*") and len(card) == 5:
        return card
    if len(card) >= 4:
        return f"*{card[-4:]}"
    return card  # если номер короче, возвращаем как есть
