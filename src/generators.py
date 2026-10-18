from typing import Generator


def filter_by_currency(transactions_list: list | dict, currency: str) -> Generator:
    """
    Функция filter_by_currency принимает список словарей на вход
    и возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)
    """
    for x in transactions_list:
        try:
            if x["operationAmount"]["currency"]["code"] == currency:
                yield x
        except KeyError, ValueError, TypeError:
            continue


def transaction_descriptions(transactions_list: list | dict) -> Generator:
    """
    Функция-генератор transaction_descriptions принимает на вход список словарей с транзакциями,
    использует yield для генерации значений по запросу и возвращает описание каждой операции по очереди
    """
    for transaction in transactions_list:
        # ВАЖНО: Весь код, который может вызвать ошибку доступа к ключам,
        # должен находиться ВНУТРИ блока try.
        try:
            # # этой строкой мы выводим ТОЛЬКО инфо из 'description', а не всю запись
            description = transaction["description"]
            # Если мы все еще здесь, значит ключ найден, можно отдавать значение
            yield description
        except KeyError, ValueError, TypeError:
            continue


def card_number_generator(start: int | str = 0, stop: int | str = 0) -> Generator:
    """
    Генератор card_number_generator принимает значения start и stop в качестве аргументов
    выдает номера банковских карт в формате XXXX XXXX XXXX XXXX. Генератор может сгенерировать номера карт
    в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999
    """
    try:
        # Преобразуем входные данные в числа, чтобы точно число
        s_start = int(start)
        s_stop = int(stop)
    except ValueError, TypeError:
        # Если переданы совсем некорректные данные, выходим
        return
    if s_start >= 0 and s_stop > 0 and s_start <= s_stop and s_stop <= 10**16:
        for number in range(s_start, s_stop + 1):
            card_number = str(number).zfill(16)  # заполняем нулями до 16 цифр
            formatted_card_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
            yield formatted_card_number


#
# for card_number in card_number_generator (0,1): #(9999999999999998,10000000000000000):
#      print(card_number)
# Пример использования функции:
# >>> 0000 0000 0000 0001
#     0000 0000 0000 0002
#     0000 0000 0000 0003
#     0000 0000 0000 0004
#     0000 0000 0000 0005
#     '''
#
#
#
# if __name__ == '__main__':
#     transactions_2 = [] # is null
#     transactions_3 = [{ # is error
#             "id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689",
#             "operationAmount": {"amount": "67314.70",
#                 "currency": {"name": "%", "code": "%"}},
#             "description": None, "from": "Visa Platinum 1246377376343588",
#             "to": "Счет 14211924144426031657"        },
#         {   "id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689",
#             "operationAmount": {"amount": "67314.70",
#                                 "currency": ''},
#             "from": "Visa Platinum 1246377376343588",
#             "to": "Счет 14211924144426031657"        }]
#
#     transactions = [ # is_valid
#         {
#             "id": 939719570,
#             "state": "EXECUTED",
#             "date": "2018-06-30T02:08:58.425572",
#             "operationAmount": {
#                 "amount": "9824.07",
#                 "currency": {
#                     "name": "USD",
#                     "code": "USD"
#                 }
#             },
#             "description": "Перевод организации",
#             "from": "Счет 75106830613657916952",
#             "to": "Счет 11776614605963066702"
#         },
#         {
#             "id": 142264268,
#             "state": "EXECUTED",
#             "date": "2019-04-04T23:20:05.206878",
#             "operationAmount": {
#                 "amount": "79114.93",
#                 "currency": {
#                     "name": "USD",
#                     "code": "USD"
#                 }
#             },
#             "description": "Перевод со счета на счет",
#             "from": "Счет 19708645243227258542",
#             "to": "Счет 75651667383060284188"
#         },
#         {
#             "id": 873106923,
#             "state": "EXECUTED",
#             "date": "2019-03-23T01:09:46.296404",
#             "operationAmount": {
#                 "amount": "43318.34",
#                 "currency": {
#                     "name": "руб.",
#                     "code": "RUB"
#                 }
#             },
#             "description": "Перевод со счета на счет",
#             "from": "Счет 44812258784861134719",
#             "to": "Счет 74489636417521191160"
#         },
#         {
#             "id": 895315941,
#             "state": "EXECUTED",
#             "date": "2018-08-19T04:27:37.904916",
#             "operationAmount": {
#                 "amount": "56883.54",
#                 "currency": {
#                     "name": "USD",
#                     "code": "USD"
#                 }
#             },
#             "description": "Перевод с карты на карту",
#             "from": "Visa Classic 6831982476737658",
#             "to": "Visa Platinum 8990922113665229"
#         },
#         {
#             "id": 594226727,
#             "state": "CANCELED",
#             "date": "2018-09-12T21:27:25.241689",
#             "operationAmount": {
#                 "amount": "67314.70",
#                 "currency": {
#                     "name": "руб.",
#                     "code": "RUB"
#                 }
#             },
#             "description": "Перевод организации",
#             "from": "Visa Platinum 1246377376343588",
#             "to": "Счет 14211924144426031657"
#         }]
# выполнение кода
#     usd_transactions = filter_by_currency(transactions, "USD")
#     print("--- 1. filter_by_currency_ Работа с итератором через цикл for (все элементы) ---")
#     for one_transaction in usd_transactions:
#         print(one_transaction)
#
#     print("\n--- 2. filter_by_currency_ Работа через for _ in range(2) (ограниченный вывод) ---")
#     usd_transactions = filter_by_currency(transactions, "EUR")
#     # используем range(2), чтобы выполнить тело цикла ровно 2 раза
#     my_range = 4
#     for _ in range(my_range):
#         try:
#             # Внутри цикла мы принудительно запрашиваем следующий элемент
#             print(next(usd_transactions))
#         except StopIteration:
#             # Если в генераторе меньше 2-х нужных элементов, выйдет ошибка StopIteration
#             print(f"В списке меньше {my_range} транзакций с такой валютой")
#             break
#
#     print("\n--- 3. filter_by_currency_ Работа через next() (ручной вызов) ---")
#     usd_transactions = filter_by_currency(transactions, "RUB")
#     try:
#         print("Первая:", next(usd_transactions))
#         print("Вторая:", next(usd_transactions))
#         print("Третья:", next(usd_transactions))
#     except StopIteration:
#         print("Больше транзакций не найдено")
#
#     print("\n--- 4. filter_by_currency_ Работа через next() (совсем ручной вызов) ---")
#     usd_transactions = filter_by_currency(transactions_2, "USD")
#     print("Первая:", next(usd_transactions))
#     print("Вторая:", next(usd_transactions))
#     print("Третья:", next(usd_transactions))
#     print("Четвертая:", next(usd_transactions))
#
#
#     print("\n--- 5. _transaction_descriptions Работа через for _ in range(4) (ограниченный вывод) ---")
#     descriptions = transaction_descriptions(transactions_2)
#     # используем range(5), чтобы выполнить тело цикла ровно 5 раз
#     my_range = 6
#
#     for _ in range(my_range):
#         try:
#             # Внутри цикла мы принудительно запрашиваем следующий элемент
#             print(next(descriptions))
#         except StopIteration:
#             # Если в генераторе меньше 5 нужных элементов, выйдет ошибка StopIteration
#             print(f"В списке меньше {my_range} транзакций")
#             break
#
# ''' Пример использования функции^
#     descriptions = transaction_descriptions(transactions)
#         for _ in range(5):
#         print(next(descriptions))
#
#     >>> Перевод организации
#         Перевод со счета на счет
#         Перевод со счета на счет
#         Перевод с карты на карту
#         Перевод организации
#     '''
#
# def card_number_generator (start:int|str=0, stop:int|str=0)-> Generator:
#     """
#     Генератор card_number_generator принимает значения start и stop в качестве аргументов
#     выдает номера банковских карт в формате XXXX XXXX XXXX XXXX. Генератор может сгенерировать номера карт
#     в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999
#     """
# for card_number in card_number_generator(9995,10001):
#      print(card_number)
# Пример использования функции:
# >>> 0000 0000 0000 0001
#     0000 0000 0000 0002
#     0000 0000 0000 0003
#     0000 0000 0000 0004
#     0000 0000 0000 0005
#     '''
