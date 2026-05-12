import pytest
from src.processing import filter_by_state, sort_by_date
# @pytest.fixture()
# def dict_state() -> list[dict]:
#     # для def filter_by_state(dict_state: List[Dict], state: str = "EXECUTED") -> List[Dict]^ in processing.py
#     # для def sort_by_date(dict_state: List[Dict], sort_date: bool = True) -> List[Dict]^  in processing.py
#     return [
#         {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#         {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
#         {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
#         {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
#     ]
#
# Функция filter_by_state:
# - Тестирование фильтрации списка словарей по заданному статусу state.
# - Проверка работы функции при отсутствии словарей с указанным статусом state в списке.
# - Параметризация тестов для различных возможных значений статуса state. state = 'EXECUTED' по умолчанию
def test_filter_by_state_st_none(dict_state: list[dict]) -> None:
    expected = [
        ({"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}),
        ({"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}),
    ]
    assert filter_by_state(dict_state) == expected


def test_filter_by_state_st_canceled(dict_state: list[dict]) -> None:
    expected = [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    assert filter_by_state(dict_state, state="CANCELED") == expected


def test_filter_by_state_st_error_1(dict_state: list[dict]) -> None:
    with pytest.raises(ValueError, match="статус отсутствует или указан неверно"):
        filter_by_state(dict_state, state="CANC")


def test_filter_by_state_st_error_2() -> None:
    with pytest.raises(ValueError, match="отсутствие словарей"):
        filter_by_state([])


@pytest.mark.parametrize(
    # разные неточности статуса
    "defolt_state, value_error",
    [
        ("CANCELD", "статус отсутствует или указан неверно"),
        ("EXECUTEDD", "статус отсутствует или указан неверно"),
        ("canceled", "статус отсутствует или указан неверно"),
    ],
)
def test_filter_by_state_errors_with_index_fixture_dict_state(
    dict_state: list[dict], defolt_state: str, value_error: str
) -> None:
    """Берем запись из фикстуры по индексу, проверяем ошибку статуса"""
    # индекс от фикстуры!!!!!!!! Внутри теста фикстура уже превратилась в список.
    index_in_fixture = [dict_state[0]]

    # Если искать в этой записи другой статус --> ошибка
    with pytest.raises(ValueError, match=value_error):
        filter_by_state(index_in_fixture, state=defolt_state)


# Функция `sort_by_date`
# - Сортировка по убыванию/возрастанию
# - Одинаковые даты (стабильность сортировки)
# - Невалидные форматы дат
# - Отсутствующее поле даты
#
# Функция sort_by_date:
# - Тестирование сортировки списка словарей по датам в порядке убывания и возрастания.
# - Проверка корректности сортировки при одинаковых датах.
# - Тесты на работу функции с некорректными или нестандартными форматами дат.


def test_sort_by_date_as_default_true(dict_state: list[dict]) -> None:
    expected = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert sort_by_date(dict_state) == expected


def test_sort_by_date_as_false(dict_state: list[dict]) -> None:
    expected = [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]
    assert sort_by_date(dict_state, False) == expected


def test_sort_by_date_identical_dates() -> None:
    dict_test_1 = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-09-12T08:21:33.419441"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-09-12T02:08:58.425572"},
    ]
    # одинаковые даты: отбор по чч,мм.сек - работает))
    expected = [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-09-12T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-09-12T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]
    assert sort_by_date(dict_test_1, False) == expected


# Проверка работы с пустым списком: ничего не возвращает, в ошибку не падает
def test_sort_by_date_empty_list() -> None:
    assert sort_by_date([]) == []


@pytest.mark.parametrize(
    "invalid_data, expected_id_order",
    [
        # 1. Пустые строки вместо дат # Пустая строка всегда "меньше" любой другой при сортировке
        # при reverse=True (по умолчанию) пустая будет в конце
        (
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2019-09-12T02:08:58.425572"},
                {"id": 939719571, "state": "EXECUTED", "date": ""},
            ],
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2019-09-12T02:08:58.425572"},
                {"id": 939719571, "state": "EXECUTED", "date": ""},
            ],
        ),
        # 2. Отсутствие ключа 'date' (вызовет ошибку KeyError)
        (
            [
                {"id": 939719571, "state": "EXECUTED"},
                {"id": 939719570, "state": "EXECUTED", "date": "2019-09-12T02:08:58.425572"},
            ],
            None,
        ),
    ],
)
def test_sort_by_date_edge_cases(invalid_data: list[dict], expected_id_order: list[dict] | None) -> None:
    if expected_id_order is None:
        # Проверяем, что при отсутствии ключа 'date' падает ошибка
        with pytest.raises(KeyError, match="Ошибка: дата"):
            sort_by_date(invalid_data)
    else:
        # Проверяем порядок сортировки с пустыми датами
        assert sort_by_date(invalid_data) == expected_id_order
