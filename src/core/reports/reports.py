from typing import Dict
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def generate_spending_report(df: pd.DataFrame) -> Dict[str, float]:
    """
    Генерирует отчёт по тратам за последние 3 месяца по категориям.
    """
    report: Dict[str, float] = {}

    # Предполагается, что df уже отфильтрован по дате
    grouped = df.groupby("Категория")["Сумма операции"].sum()

    for category, total in grouped.items():
        report[category] = float(total)

    logger.debug(f"Сформирован отчёт по тратам: {report}")

    return report
