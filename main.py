import logging
from src.core.transactions import load_transactions
from src.core.services.services import calculate_cashback, round_transactions
from src.core.reports.reports import generate_spending_report
from src.api.finance_client import get_currency_rates

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    )

    # Загрузка и обработка данных
    df = load_transactions("data/raw/operations.xlsx")
    df = round_transactions(df, step=10)
    cashback = calculate_cashback(df)
    report = generate_spending_report(df)
    currency_rates = get_currency_rates()

    # Вывод результатов
    print("📊 Краткий отчёт:")
    print(f"💰 Суммарный кешбэк: {cashback:.2f} ₽\n")

    print("📈 Курсы валют (по данным Twelve Data):")
    for pair, rate in currency_rates.items():
        print(f"  {pair}: {rate:.2f}")

    print("\n📂 Отчёт по тратам (за 3 последних месяца):")
    for category, amount in report.items():
        print(f"  {category}: {amount:.2f} ₽")

if __name__ == "__main__":
    main()
