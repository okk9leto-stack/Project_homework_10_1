import re
from collections import Counter


def process_bank_search(transactions_list: list[dict], search_text: str) -> list[dict]:
    """Возвращает операции, в описании которых есть строка поиска."""
    pattern = re.compile(search_text, re.IGNORECASE)

    return [transaction for transaction in transactions_list if pattern.search(transaction.get("description", ""))]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Функция принимает список словарей с данными о банковских операциях и список категорий операций,
    и возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    """
    all_categories = [operation.get("description") for operation in data]
    counter = Counter(all_categories)

    result = {}

    for category in categories:
        result[category] = counter.get(category, 0)

    return result


def filter_by_currency(transactions_list: list | dict, currency: str = "ALL") -> list | dict:
    """
    Функция принимает на вход список словарей с транзакциями и валюту,
    возвращает список словарей с транзакциями по выбранной валюте.
    Если валюта не выбрана, возвращает первоначальный список с транзакциями во всех валютах
    """
    if currency == "ALL":
        return transactions_list

    return [
        transaction
        for transaction in transactions_list
        if transaction["operationAmount"]["currency"]["code"] == currency
    ]

#
# if __name__ == "__main__":
#     transactions = [  # is_valid
#         {
#             "id": 939719570,
#             "state": "EXECUTED",
#             "date": "2018-06-30T02:08:58.425572",
#             "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод организации",
#             "from": "Счет 75106830613657916952",
#             "to": "Счет 11776614605963066702",
#         },
#         {
#             "id": 142264268,
#             "state": "EXECUTED",
#             "date": "2019-04-04T23:20:05.206878",
#             "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод со счета на счет",
#             "from": "Счет 19708645243227258542",
#             "to": "Счет 75651667383060284188",
#         },
#         {
#             "id": 873106923,
#             "state": "EXECUTED",
#             "date": "2019-03-23T01:09:46.296404",
#             "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
#             "description": "Перевод со счета на счет",
#             "from": "Счет 44812258784861134719",
#             "to": "Счет 74489636417521191160",
#         },
#         {
#             "id": 895315941,
#             "state": "EXECUTED",
#             "date": "2018-08-19T04:27:37.904916",
#             "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод с карты на карту",
#             "from": "Visa Classic 6831982476737658",
#             "to": "Visa Platinum 8990922113665229",
#         },
#         {
#             "id": 594226727,
#             "state": "CANCELED",
#             "date": "2018-09-12T21:27:25.241689",
#             "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
#             "description": "Перевод организации",
#             "from": "Visa Platinum 1246377376343588",
#             "to": "Счет 14211924144426031657",
#         },
#     ]
#
#     rub_transactions = filter_by_currency(transactions, "RUB")
#     for one_transaction in rub_transactions:
#         print(one_transaction)
#
#     search_transactions = process_bank_search(transactions, "Переводs")
#     for one_transaction in search_transactions:
#         print(one_transaction)
#
#     states_count = process_bank_operations(transactions, ["Переводы организации", "Перевод с карты на карту"])
#     print(states_count)
