import pytest

from src.search import filter_by_currency_csv_xlsx
from src.search import filter_by_currency_json
from src.search import process_bank_operations
from src.search import process_bank_search


def test_process_bank_search_finds_operations_by_description() -> None:
    transactions_list = [
        {"description": "Перевод от Иванова", "amount": 1000},
        {"description": "Оплата продуктов", "amount": 500},
        {"description": "Перевод за квартиру", "amount": 20000},
    ]

    result = process_bank_search(transactions_list, "перевод")

    assert result == [
        {"description": "Перевод от Иванова", "amount": 1000},
        {"description": "Перевод за квартиру", "amount": 20000},
    ]


def test_process_bank_search_is_case_insensitive() -> None:
    transactions_list = [
        {"description": "Перевод от Иванова", "amount": 1000},
        {"description": "ПЕРЕВОД за квартиру", "amount": 20000},
        {"description": "Оплата продуктов", "amount": 500},
    ]

    result = process_bank_search(transactions_list, "перевод")

    assert len(result) == 2


def test_process_bank_search_returns_empty_list_if_nothing_found() -> None:
    transactions_list = [
        {"description": "Оплата продуктов", "amount": 500},
        {"description": "Оплата интернета", "amount": 1000},
    ]

    result = process_bank_search(transactions_list, "перевод")

    assert result == []


def test_process_bank_search_returns_empty_list_for_empty_data() -> None:
    result = process_bank_search([], "перевод")

    assert result == []


# from src.search import process_bank_operations


def test_process_bank_operations() -> None:
    data = [
        {"description": "Перевод организации", "amount": 1000},
        {"description": "Оплата", "amount": 500},
        {"description": "Перевод со счета на счет", "amount": 2000},
        {"description": "Оплата", "amount": 300},
        {"description": "Перевод с карты на карту", "amount": 1500},
    ]

    categories = ["Перевод организации", "Оплата"]

    result = process_bank_operations(data, categories)

    assert result == {
        "Перевод организации": 1,
        "Оплата": 2,
    }


def test_process_bank_operations_category_not_found() -> None:
    data = [
        {"description": "Перевод", "amount": 1000},
        {"description": "Оплата", "amount": 500},
    ]

    categories = ["Перевод", "Снятие"]

    result = process_bank_operations(data, categories)

    assert result == {
        "Перевод": 1,
        "Снятие": 0,
    }


def test_process_bank_operations_empty_data() -> None:
    result = process_bank_operations([], ["Перевод", "Оплата"])

    assert result == {
        "Перевод": 0,
        "Оплата": 0,
    }


def test_process_bank_operations_empty_categories() -> None:
    data = [
        {"description": "Перевод", "amount": 1000},
        {"description": "Оплата", "amount": 500},
    ]

    result = process_bank_operations(data, [])

    assert result == {}


# from src.search import filter_by_currency_json


@pytest.fixture
def transactions() -> list[dict]:
    return [
        {"id": 1, "operationAmount": {"amount": "1000.00", "currency": {"code": "USD", "name": "Доллар США"}}},
        {"id": 2, "operationAmount": {"amount": "2000.00", "currency": {"code": "EUR", "name": "Евро"}}},
        {"id": 3, "operationAmount": {"amount": "500.00", "currency": {"code": "USD", "name": "Доллар США"}}},
    ]


def test_filter_by_currency_json_usd(transactions: list[dict]) -> None:
    """Проверяем фильтрацию транзакций по USD."""
    result = filter_by_currency_json(transactions, "USD")

    assert len(result) == 2


def test_filter_by_currency_json_eur(transactions: list[dict]) -> None:
    """Проверяем фильтрацию транзакций по EUR."""
    result = filter_by_currency_json(transactions, "EUR")

    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_currency_json_all(transactions: list[dict]) -> None:
    """Проверяем возврат всех транзакций по умолчанию."""
    result = filter_by_currency_json(transactions)

    assert result == transactions


def test_filter_by_currency_json_no_matches(transactions: list[dict]) -> None:
    """Проверяем валюту, которой нет в списке."""
    result = filter_by_currency_json(transactions, "GBP")

    assert result == []


def test_filter_by_currency_json_empty_list() -> None:
    """Проверяем работу с пустым списком транзакций."""
    assert filter_by_currency_json([], "USD") == []
    assert filter_by_currency_json([]) == []


@pytest.fixture
def transactions_csv_xlsx() -> list[dict]:
    return [
        {"id": 1, "currency_code": "USD"},
        {"id": 2, "currency_code": "EUR"},
        {"id": 3, "currency_code": "USD"},
        {"id": 4, "currency_code": "RUB"},
    ]


def test_filter_by_currency_csv_xlsx_usd(
    transactions_csv_xlsx: list[dict],
) -> None:
    result = filter_by_currency_csv_xlsx(transactions_csv_xlsx, "USD")

    assert len(result) == 2
    assert [item["id"] for item in result] == [1, 3]


def test_filter_by_currency_csv_xlsx_eur(
    transactions_csv_xlsx: list[dict],
) -> None:
    result = filter_by_currency_csv_xlsx(transactions_csv_xlsx, "EUR")

    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_currency_csv_xlsx_rub(
    transactions_csv_xlsx: list[dict],
) -> None:
    result = filter_by_currency_csv_xlsx(transactions_csv_xlsx, "RUB")

    assert len(result) == 1
    assert result[0]["id"] == 4


def test_filter_by_currency_csv_xlsx_all(
    transactions_csv_xlsx: list[dict],
) -> None:
    result = filter_by_currency_csv_xlsx(transactions_csv_xlsx, "ALL")

    assert result == transactions_csv_xlsx


def test_filter_by_currency_csv_xlsx_default_currency(
    transactions_csv_xlsx: list[dict],
) -> None:
    result = filter_by_currency_csv_xlsx(transactions_csv_xlsx)

    assert result == transactions_csv_xlsx


def test_filter_by_currency_csv_xlsx_no_matches(
    transactions_csv_xlsx: list[dict],
) -> None:
    result = filter_by_currency_csv_xlsx(transactions_csv_xlsx, "GBP")

    assert result == []


def test_filter_by_currency_csv_xlsx_empty_list() -> None:
    assert filter_by_currency_csv_xlsx([], "USD") == []
    assert filter_by_currency_csv_xlsx([], "ALL") == []
    assert filter_by_currency_csv_xlsx([]) == []
