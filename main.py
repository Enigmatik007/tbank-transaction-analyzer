import logging
import json
from src.core.transactions import load_transactions
from src.core.services.services import profitable_cashback_categories
from src.core.reports.reports import spending_by_category
from src.api.finance_client import get_currency_rates, get_stock_prices


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    )

    # Загрузка и обработка данных
    df = load_transactions("data/raw/operations.xlsx")

    # Получаем последний месяц и год из данных
    last_date = df["Дата операции"].max()
    year = last_date.year
    month = last_date.month

    # Расчет кешбэка за последний месяц
    cashback = profitable_cashback_categories(
        df.to_dict(orient="records"),
        year=year,
        month=month
    )

    # Отчёт по категории "Супермаркеты" за последние 3 месяца от последней даты
    report = spending_by_category(df, category="Супермаркеты", date=last_date.strftime("%Y-%m-%d"))

    # Получение курсов валют
    currency_rates_list = get_currency_rates()
    # Преобразуем список словарей в удобный словарь
    currency_rates = {item["currency"]: item["rate"] for item in currency_rates_list}

    # Получение цен акций
    stock_prices = get_stock_prices()

    # Формируем итоговый словарь для JSON
    result = {
        "cashback": cashback,
        "spending_report": report,
        "currency_rates": currency_rates_list,
        "stock_prices": stock_prices,
    }

    # Печать красиво отформатированного JSON
    print("📋 JSON-ответ:")
    print(json.dumps(result, ensure_ascii=False, indent=4))

    # Краткий читаемый вывод
    print("\n📊 Кешбэк по категориям за {}/{}:".format(month, year))
    for category, amount in cashback.items():
        print(f"  {category}: {amount:.2f} ₽")

    print("\n📈 Курсы валют (по данным Twelve Data):")
    for pair, rate in currency_rates.items():
        print(f"  {pair}: {rate:.2f}")

    print("\n📈 Цены акций (S&P 500):")
    for item in stock_prices:
        print(f"  {item['stock']}: {item['price']:.2f}")

    print("\n📂 Отчёт по тратам (Супермаркеты за последние 3 месяца):")
    for period, amount in report.items():
        print(f"  {period}: {amount:.2f} ₽")


if __name__ == "__main__":
    main()

