import pytest

# from src.masks import get_mask_account
# from src.masks import get_mask_card_number
from src.widget import get_date
from src.widget import mask_account_card

# @pytest.fixture()
# def date_full_format() -> str:  # для def get_date(date_in_full_format: str) -> str^ in widget.py
#     return "2024-03-11T02:26:18.671407"

# Функция mask_account_card:
# - Тесты для проверки, что функция корректно распознает и применяет нужный тип маскировки
#  в зависимости от типа входных данных (карта или счет).
# - Параметризованные тесты с разными типами карт и счетов для проверки универсальности функции.
# - Тестирование функции на обработку некорректных входных данных и проверка ее устойчивости к ошибкам.


def test_mask_account_card_norm_card() -> None:
    # обработка корректной записи для карты
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"


def test_mask_account_card_norm_acc() -> None:
    # обработка корректной записи для счета
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


@pytest.mark.parametrize(
    "card_acc_number, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ],
)
def test_mask_account_card_parametrize(card_acc_number: str, expected: str) -> None:
    assert mask_account_card(card_acc_number) == expected


# пробел или пусто
def test_mask_account_card_whitespace() -> None:
    with pytest.raises(ValueError, match="введите реквизиты карты|счета"):
        mask_account_card(" ")


# другие нестандартные случаи ввода даты, влияющие на итоговую дату
def test_mask_account_card_defolt_1() -> None:
    with pytest.raises(ValueError, match="некорректные реквизиты"):
        mask_account_card("Счет 3538303347")


def test_mask_account_card_defolt_2() -> None:
    with pytest.raises(ValueError, match="некорректные реквизиты"):
        mask_account_card("Счет --")


@pytest.mark.parametrize(
    "invalid_num",
    [
        "Счет 3538303347",  # Слишком короткий
        "Счет --",  # Символы вместо цифр
    ],
)
def test_mask_account_card_errors(invalid_num: str) -> None:
    # ожидаем ValueError
    with pytest.raises(ValueError, match="некорректные реквизиты"):
        mask_account_card(invalid_num)


# Функция get_date:
# - Тестирование правильности преобразования даты.
# - Проверка работы функции на различных входных форматах даты, включая граничные случаи
# и нестандартные строки с датами.
# - Проверка, что функция корректно обрабатывает входные строки, где отсутствует дата.
# ```


def test_get_date_norm(date_full_format: str) -> None:  # с фикстурой
    # обработка корректной записи
    assert get_date(date_full_format) == "11.03.2024"


def test_get_date_whitespace_ok() -> None:  # c assert
    # маркировка корректной даты, но с использованием пробелов
    assert get_date("2024-03-11 T 02:26:18.671407") == "11.03.2024"


# пробел или пусто
def test_get_date_whitespace_1() -> None:
    with pytest.raises(ValueError, match="Вы не ввели дату"):
        get_date(" ")


def test_get_date_null() -> None:
    with pytest.raises(ValueError, match="Вы не ввели дату"):
        get_date("")


# другие нестандартные случаи ввода даты, влияющие на итоговую дату
def test_get_date_defolt_1() -> None:
    with pytest.raises(ValueError, match="формат даты некорректный"):
        get_date(" -")


def test_get_date_defolt_2() -> None:
    with pytest.raises(ValueError, match="формат даты некорректный"):
        get_date("2024-53-11T02:26:18.671407")


def test_get_date_defolt_3() -> None:
    with pytest.raises(ValueError, match="формат даты некорректный"):
        get_date("2024-03-51T02:26:18.671407")


def test_get_date_defolt_4() -> None:
    with pytest.raises(ValueError, match="формат даты некорректный"):
        get_date("2024-03-1T02:26:18.671407")
