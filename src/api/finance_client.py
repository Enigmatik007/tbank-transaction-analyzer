# src/api/finance_client.py

import os
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()  # Загружаем .env

def get_currency_rates() -> Dict[str, float]:
    """Получает актуальные курсы валют с Twelve Data API."""
    api_key = os.getenv("TWELVE_DATA_API_KEY")
    if not api_key:
        raise ValueError("TWELVE_DATA_API_KEY не найден в .env")

    url = "https://api.twelvedata.com/exchange_rate"
    result = {}

    for symbol in ["USD/RUB", "EUR/RUB"]:
        from_symbol, to_symbol = symbol.split("/")
        response = requests.get(url, params={"symbol": symbol, "apikey": api_key})
        data = response.json()
        result[f"{from_symbol}_{to_symbol}"] = float(data["rate"])

    return result
