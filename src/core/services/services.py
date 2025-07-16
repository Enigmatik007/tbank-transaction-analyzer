import logging
import pandas as pd

logger = logging.getLogger(__name__)


def calculate_cashback(df: pd.DataFrame) -> float:
    """Рассчитывает суммарный кешбэк (1% от суммы операций)."""
    if df.empty:
        logger.info("Передан пустой DataFrame — кешбэк равен 0.")
        return 0.0

    # Заменяем пустые значения на 0, приводим к float
    cashback_series = pd.to_numeric(df["Кэшбэк"], errors="coerce").fillna(0.0)
    cashback_sum = cashback_series.sum()

    logger.debug(f"Рассчитан кешбэк: {cashback_sum}")
    return float(cashback_sum)


def round_transactions(df: pd.DataFrame, step: int) -> pd.DataFrame:
    """
    Округляет сумму операции с округлением на инвесткопилку до ближайшего 'step'.
    """
    def round_value(x: float) -> float:
        if pd.isna(x):
            return 0.0
        remainder = x % step
        return x + (step - remainder) if remainder != 0 else x

    df = df.copy()
    df["Сумма операции с округлением"] = df["Сумма операции"].apply(round_value)

    logger.debug(f"Применено округление с шагом {step} к {len(df)} транзакциям.")
    return df
