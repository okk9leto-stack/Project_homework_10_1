import pytest

from src.generators import filter_by_currency
from src.generators import transaction_descriptions

# from src.generators import card_number_generator


def test_filter_by_currency_rub(transactions: list | dict) -> None:
    """
    Функция filter_by_currency принимает список словарей на вход
    и возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)
    """
    usd_transactions = filter_by_currency(transactions, "RUB")  # transactions фикстура
    assert (next(usd_transactions)) == {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    }
    assert (next(usd_transactions)) == {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    }
    # получили первое значение
    # далее ожидаем, что следующий вызов вызовет ошибку
    with pytest.raises(StopIteration):
        next(usd_transactions)


def test_filter_by_currency_usd(transactions: list | dict) -> None:
    """
    Функция filter_by_currency принимает список словарей на вход
    и возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)
    """
    usd_transactions = filter_by_currency(transactions, "USD")  # transactions фикстура
    assert (next(usd_transactions)) == {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    assert (next(usd_transactions)) == {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }
    assert (next(usd_transactions)) == {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    }
    # получили 1-3 значение
    # далее ожидаем, что следующий вызов вызовет ошибку
    with pytest.raises(StopIteration):
        next(usd_transactions)


def test_filter_by_currency_eur(transactions: list | dict) -> None:
    """
    Функция filter_by_currency принимает список словарей на вход
    и возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)
    """
    usd_transactions = filter_by_currency(transactions, "EUR")  # transactions фикстура
    # ожидаем ошибку
    with pytest.raises(StopIteration):
        next(usd_transactions)


def test_filter_by_currency_null(transactions_null: list = []) -> None:
    """
    Функция filter_by_currency принимает список словарей на вход
    и возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)
    """
    usd_transactions = filter_by_currency(transactions_null, "USD")  # transactions фикстура
    # ожидаем ошибку
    with pytest.raises(StopIteration):
        next(usd_transactions)


@pytest.mark.parametrize(
    "input_data, currency",
    [
        ([{"id": 1, "operationAmount": {"currency": {"code": "RUB"}}}], "RUR"),  # Случай 1: Валюты нет в списке (RUR)
        ([], "USD"),  # Случай 2: Пустой список транзакций
        ([{"bad_key": "data"}], "USD"),  # Случай 3: Список с битыми данными
    ],
)
def test_filter_by_currency_stop_iteration(input_data: list, currency: str) -> None:
    """Тестируем все случаи, когда итератор должен сразу выдать StopIteration"""
    usd_transactions = filter_by_currency(input_data, currency)
    with pytest.raises(StopIteration):
        next(usd_transactions)


@pytest.mark.parametrize(
    "input_data, currency, expected_count",
    [
        # 1. KeyError: отсутствует главный ключ "operationAmount"
        ([{"id": 1, "state": "EXECUTED"}], "USD", 0),
        # 2. KeyError: отсутствует вложенный ключ "currency"
        ([{"operationAmount": {"amount": "100"}}], "USD", 0),
        # 3. TypeError: вместо словаря в списке лежит число или None
        ([123, None, {"id": 2}], "USD", 0),
        # 4. TypeError: промежуточное значение равно None (нельзя взять ключ ['code'])
        ([{"operationAmount": {"currency": None}}], "USD", 0),
        # 5. Смешанные данные: "битый" объект + "хороший" объект
        # Проверяет, что 'continue' не ломает цикл и мы доходим до валидных данных
        ([{"bad": "data"}, {"operationAmount": {"currency": {"code": "USD"}}}], "USD", 1),
        # 6. ValueError: в структуре ['code'] НЕ строка (int).
        ([{"operationAmount": {"currency": {"code": 123}}}], "USD", 0),
    ],
)
def test_filter_by_currency_errors_cases(input_data: list, currency: str, expected_count: int) -> None:
    """
    Тестируем пропуск некорректных данных для ветки except (KeyError, ValueError, TypeError).
    """
    result_list = list(filter_by_currency(input_data, currency))
    assert len(result_list) == expected_count


def test_transaction_descriptions_standard(transactions: list | dict) -> None:
    """
    Тест стандартного вывода значений из descriptions/
    Тестируем выдачу StopIteration при запросе транзакций больше, чем их есть
    """
    descriptions = transaction_descriptions(transactions)  # transactions фикстура
    assert (next(descriptions)) == "Перевод организации"
    assert (next(descriptions)) == "Перевод со счета на счет"
    assert (next(descriptions)) == "Перевод со счета на счет"
    assert (next(descriptions)) == "Перевод с карты на карту"
    assert (next(descriptions)) == "Перевод организации"
    # далее ожидаем, что следующий вызов вызовет ошибку StopIteration (в списке только 5 транзакций)
    with pytest.raises(StopIteration):
        next(descriptions)


def test_transaction_descriptions_null(transactions_null: list = []) -> None:
    """
    Тест пустого списка
    """
    descriptions = transaction_descriptions(transactions_null)  # transactions фикстура
    # ожидаем ошибку
    with pytest.raises(StopIteration):
        next(descriptions)  # transactions фикстура


@pytest.mark.parametrize(  # Тестируем прогон некорректных данных для ветки except (KeyError, ValueError, TypeError)
    "input_data_2, expected_count",
    [
        # 1. KeyError: отсутствует ключ "description"
        ([{"id": 1, "state": "EXECUTED"}], 0),
        # 2. TypeError: вместо словаря в списке лежит число или None
        ([123, None, {"id": 2}], 0),
        # 3. Смешанные данные: "битый" объект + "хороший" объект
        # Проверяет, что 'continue' не ломает цикл и мы доходим до валидных данных
        ([{"bad": "data"}, {"description": "Перевод с карты на карту"}], 1),
        # 4. При наличии ключа "description" выводит из него и None, и пустые, и числовые значения
        ([{"description": None}], 1),
        ([{"description": ""}], 1),
        ([{"description": 123}], 1),
    ],
)
def test_transaction_descriptions_errors_cases(input_data_2: list, expected_count: int) -> None:
    """
    Тестируем прогон некорректных данных для ветки except (KeyError, ValueError, TypeError).
    """
    result_list = list(transaction_descriptions(input_data_2))
    assert len(result_list) == expected_count


#     pass
#
#
# def test_card_number_generator (start, stop)-> None:
#     """
#     Генератор card_number_generator принимает значения
#     start и stop в качестве аргумента
#     """
#     pass


"""
Примеры тест-кейсов/ Тестирование функции: filter_by_currency:
- Напишите тесты, проверяющие, что функция корректно фильтрует транзакции по заданной валюте.
- Проверьте, что функция правильно обрабатывает случаи, когда транзакции в заданной валюте отсутствуют.
- Убедитесь, что генератор не завершается ошибкой при обработке пустого списка
  или списка без соответствующих валютных операций.

Примеры тест-кейсов/ Тестирование функции: transaction_descriptions:
- Проверьте, что функция возвращает корректные описания для каждой транзакции.
- Тестируйте работу функции с различным количеством входных транзакций, включая пустой список.

Примеры тест-кейсов/ Тестирование генератора: card_number_generator:
- Напишите тесты, которые проверяют, что генератор выдает правильные номера карт в заданном диапазоне.
- Проверьте корректность форматирования номеров карт.
- Убедитесь, что генератор корректно обрабатывает крайние значения диапазона и правильно завершает генерацию.
"""
