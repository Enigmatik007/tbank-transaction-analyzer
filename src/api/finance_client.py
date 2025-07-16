"""Модуль для работы с финансовыми API (курсы валют, акции)."""

import logging
import os
from typing import List, TypedDict

from dotenv import load_dotenv
import requests

load_dotenv()
logger = logging.getLogger(__name__)


class CurrencyRate(TypedDict):
    currency: str
    rate: float


class StockPrice(TypedDict):
    stock: str
    price: float


def get_currency_rates() -> List[CurrencyRate]:
    """
    Получает текущие курсы валют из Twelve Data API.

    Returns:
        List[CurrencyRate]: Список словарей с валютами и курсами.
    """
    try:
        api_key = os.getenv("TWELVE_DATA_API_KEY")
        if not api_key:
            raise ValueError("API key not found in .env")

        url = "https://api.twelvedata.com/exchange_rate"
        currencies = ["USD/RUB", "EUR/RUB"]
        result: List[CurrencyRate] = []

        for pair in currencies:
            response = requests.get(url, params={"symbol": pair, "apikey": api_key}, timeout=10)
            response.raise_for_status()
            data = response.json()
            result.append({"currency": pair.split("/")[0], "rate": float(data["rate"])})

        logger.info("Currency rates fetched successfully")
        return result

    except Exception as e:
        logger.error(f"Error fetching currency rates: {str(e)}")
        raise


def get_stock_prices() -> List[StockPrice]:
    """
    Получает текущие цены акций из Twelve Data API.

    Returns:
        List[StockPrice]: Список словарей с акциями и ценами.
    """
    try:
        api_key = os.getenv("TWELVE_DATA_API_KEY")
        if not api_key:
            raise ValueError("API key not found in .env")

        stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        result: List[StockPrice] = []

        for stock in stocks:
            response = requests.get(
                "https://api.twelvedata.com/price", params={"symbol": stock, "apikey": api_key}, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            result.append({"stock": stock, "price": float(data["price"])})

        logger.info("Stock prices fetched successfully")
        return result

    except Exception as e:
        logger.error(f"Error fetching stock prices: {str(e)}")
        raise
