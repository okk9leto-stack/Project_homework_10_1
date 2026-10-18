import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number

# @pytest.fixture  # in conftest.py
# def card_number() -> str:  # для def get_mask_card_number(number: str) -> str: in masks
#     return "7000792289606361"
#
# @pytest.fixture()  # in conftest.py
# def account_number() -> str:  # для def get_mask_account(number: str) -> str: in masks
#     return "73654108430135874305"


# Функция get_mask_card_number:
# - Тестирование правильности маскирования номера карты.
# - Проверка работы функции на различных входных форматах номеров карт,
#   включая граничные случаи и нестандартные длины номеров.
# - Проверка, что функция корректно обрабатывает входные строки, где отсутствует номер карты.


def test_get_mask_card_number_norm(card_number: str) -> None:  # с фикстурой
    # маркировка корректного номера
    assert get_mask_card_number(card_number) == "7000 79** **** 6361"


def test_get_mask_card_number_whitespace() -> None:  # c assert
    # маркировка корректного номера, но с использованием пробелов
    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "number, expected",
    [  # parametrize
        # длинный или короткий номер
        ("700079228960000000000000000006361", "Ошибка: неверная длина номера"),
        ("700079006361", "Ошибка: неверная длина номера"),
        # пробел или пусто
        (" ", "Ошибка: Вы не ввели номер карты"),
        ("", "Ошибка: Вы не ввели номер карты"),
        # слова, буквы, специальные символы в номере
        ("Maestro 7000 7922 8960 6361", "Ошибка: номер карты должен состоять только из цифр"),
        ("700079228960%361", "Ошибка: номер карты должен состоять только из цифр"),
    ],
)
def test_get_mask_card_number_not_norm(number: str, expected: str) -> None:
    assert get_mask_card_number(number) == expected


# Функция get_mask_account:
# - Тестирование правильности маскирования номера счета.
# - Проверка работы функции с различными форматами и длинами номеров счетов.
# - Проверка, что функция корректно обрабатывает входные данные, где номер счета меньше ожидаемой длины.


def test_get_mask_account_norm(account_number: str) -> None:  # с фикстурой
    # маркировка корректного номера
    assert get_mask_account(account_number) == "**4305"


def test_get_mask_account_whitespace_ok() -> None:  # c assert
    # маркировка корректного номера, но с использованием пробелов
    assert get_mask_account("7365 4108 4301 3587 4305") == "**4305"


# длинный или короткий номер
def test_get_mask_account_not20_1() -> None:
    with pytest.raises(ValueError, match="неверная длина номера"):
        get_mask_account("700079228960000000000000000006361")


def test_get_mask_account_not20_2() -> None:
    with pytest.raises(ValueError, match="неверная длина номера"):
        get_mask_account("70007922896361")


# пробел или пусто
def test_get_mask_account_whitespace_1() -> None:
    with pytest.raises(ValueError, match="Вы не ввели номер счета"):
        get_mask_account(" ")


def test_get_mask_account_null() -> None:
    with pytest.raises(ValueError, match="Вы не ввели номер счета"):
        get_mask_account("")


# слова, буквы, специальные символы в номере
def test_get_mask_account_word_1() -> None:
    with pytest.raises(ValueError, match="должен состоять только из цифр"):
        get_mask_account("Acc. 736541084301358743054")


def test_get_mask_account_word_2() -> None:
    with pytest.raises(ValueError, match="должен состоять только из цифр"):
        get_mask_account("7365410843o1358743054")


def test_get_mask_account_word_3() -> None:
    with pytest.raises(ValueError, match="должен состоять только из цифр"):
        get_mask_account("7365410843%1358743054")
