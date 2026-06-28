import datetime
import json
import os
from typing import Dict
from typing import Tuple

import requests
from dotenv import load_dotenv


def get_api_key() -> str | None:
    """Загружает переменные окружения и возвращает API_KEY."""
    load_dotenv()  # Загрузка переменных из .env-файла
    API_KEY = os.getenv("API_KEY")  # Получение значения переменной API_KEY из .env-файла
    return API_KEY


def date_date(date: str) -> str:

    try:
        # 1. Парсим строку в объект. Обратите внимание на T между датой и временем.
        date_full = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
        # 2. Форматируем объект в строку нужного вам вида (например, ДД.ММ.ГГГГ)
        date_new = date_full.strftime("%Y-%m-%d")
        return date_new
    except ValueError:
        raise ValueError("корректный формат даты: 2018-04-22T17:01:46.885252")


# Операции по конвертации валюты
# Реализована функция конвертации валюты из USD и EUR в рубли.
# Функция конвертации валюты из USD и EUR в рубли принимает на вход словарь с данными о транзакции.
# Функция конвертации валюты из USD и EUR в рубли возвращает сумму транзакции (ключ
# amount) в рублях, тип данных float.
# Если транзакция была в USD или EUR, происходит обращение к внешнему API
# для получения текущего курса валют и конвертации суммы операции в рубли.
#  {  "id": 123456789, "state": "EXECUTED", "date": "2019-04-19T12:02:30.129240",
# "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}}}
# Сокрытие чувствительных данных
# Ключи для авторизации в API конвертации валют скрыты в файле .env.
# Собран шаблон файла .env с указанием названий всех переменных, необходимых для работы приложения.
#
def currency_conversion(transaction: Dict) -> Dict | Tuple[int, Dict]:
    date_transact = date_date(transaction["date"])
    amount_transact = transaction["operationAmount"]["amount"]
    currency_transact = transaction["operationAmount"]["currency"]["code"]

    RUB_amount = 0.0
    rates = 1.0
    result_fin = {}
    status_code = None

    if currency_transact in ["USD", "EUR"]:
        # url = f"https://api.apilayer.com/exchangerates_data/{date_transact}?symbols=RUB&base={currency_transact}"
        url = f"https://api.apilayer.com/exchangerates_data/{date_transact}"
        payload = {"symbols": "RUB", "base": currency_transact}

        # Создание заголовка с кодом доступа API
        # аналогично записи headers = {"apikey": "Pmtbk5HywReubmCx0quOdEBstCPboXff"}
        headers = {"apikey": get_api_key()}

        try:
            # Отправка GET-запроса к API
            # аналогично записи на сайте: response = requests.request("GET", url, headers=headers, data=payload)
            response = requests.get(url, headers=headers, params=payload)
            status_code = response.status_code
            response.raise_for_status()

            result = response.json()
            rates = float(result["rates"]["RUB"])
            RUB_amount = rates * float(amount_transact)

            # Обработка ответа
            print(f"status_code = {status_code}")

        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            print(f"Ошибка при запросе к API курсов валют: {e}")
            return {}

    elif currency_transact == "RUB":
        RUB_amount = float(amount_transact)
        rates = 1.0

    else:
        return {}

    result_fin = {
        "rates": rates,
        "currency": currency_transact,
        "amount_transact": float(amount_transact),
        "RUB_amount": RUB_amount,
    }
    print(json.dumps(result_fin, indent=4, ensure_ascii=False))
    return result_fin


# if __name__ == "__main__":
#     print (date_date("2018-04-22 T17:01:46.885252"))
#
# if __name__ == "__main__":
#     transaction = {
#         "id": 123456789,
#         "state": "EXECUTED",
#         "date": "2019-04-19T12:02:30.129240",
#         "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
#     }
#     print(currency_conversion(transaction))
#
# { "base": "USD",
#   "date": "2026-05-01",
#   "historical": true,
#   "rates": {"RUB": 74.972586},
#   "success": true,
#   "timestamp": 1777679999}
