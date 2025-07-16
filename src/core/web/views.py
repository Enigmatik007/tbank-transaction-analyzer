import logging
from datetime import datetime

from src.api.finance_client import get_currency_rates
from src.core.transactions import load_transactions

logger = logging.getLogger(__name__)


def home_page(datetime_str: str) -> dict:
    """
    Возвращает JSON с приветствием, списком карт, топ-5 транзакциями и курсами валют.
    """
    try:
        dt = datetime.fromisoformat(datetime_str)
        hour = dt.hour
        if 5 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 18:
            greeting = "Добрый день"
        elif 18 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"

        logger.info(f"Выбрано приветствие: {greeting} (время: {datetime_str})")

        df = load_transactions()
        logger.debug(f"Загружено транзакций: {len(df)}")

        cards = sorted(set(df["Номер карты"].dropna().unique()))
        logger.debug(f"Обнаружены карты: {cards}")

        top5 = (
            df.sort_values("Дата операции", ascending=False)
            .head(5)[["Дата операция", "Описание", "Сумма операции", "Категория"]]
            .to_dict(orient="records")
        )

        rates = get_currency_rates()
        logger.debug(f"Курсы валют получены: {rates}")

        return {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top5,
            "currency_rates": rates,
        }

    except Exception as e:
        logger.exception("Ошибка при формировании данных для главной страницы")
        return {"error": str(e)}
