import pytest

from src.practic_11_2 import binary_search
from src.practic_11_2 import calculate_area
from src.practic_11_2 import check_email_1
from src.practic_11_2 import count_number_in_list
from src.practic_11_2 import merge_dicts
from src.practic_11_2 import my_slice
from src.practic_11_2 import sum_divisible_by_3_or_5


def test_sum_divisible_by_3_or_5() -> None:
    """
    Функция принимает на вход список чисел и возвращает сумму всех элементов списка,
    которые делятся на 3 или 5 без остатка.
    """
    assert sum_divisible_by_3_or_5([1, 2, 3]) == 3
    assert sum_divisible_by_3_or_5([1, 2, 3, 4, 5]) == 8
    assert sum_divisible_by_3_or_5([]) == 0
    assert sum_divisible_by_3_or_5([1, 2, 4, 7, 8]) == 0
    assert sum_divisible_by_3_or_5([-3, -5, -6, -10, -12]) == -36


def test_check_email_1_with_valid_email() -> None:
    """
    проверяет, что функция check_email корректно обрабатывает правильно написанный email
    """
    assert check_email_1("email@mail.ru") == True


def test_check_email_1_with_invalid_email() -> None:
    """
    проверяет, что функция check_email корректно обрабатывает неправильно написанный email
    """
    assert check_email_1("email@mail.") == False
    assert check_email_1("email.mail@u") == False
    assert check_email_1("test@.com") == False
    assert check_email_1("test@example") == False
    assert check_email_1("testexample.com") == False
    assert check_email_1("@example.com") == False
    # assert check_email_1("test@exam_ple.com") == False


def test_check_email_1_with_empty_email() -> None:
    """
    проверяет, что функция check_email корректно обрабатывает пустой email
    """
    assert check_email_1("") == False


# 2. Фикстура для pytest (использует эти данные)
@pytest.fixture()
def lst_of_numberss() -> list[int]:
    return [1, 2, 3, 4, 5, 6, 2, 4, 7, 9, 3, 8, 4, 4, 4, 4, 4, 1]


@pytest.fixture
def empty_list():
    return []


@pytest.fixture
def list_with_one_element():
    return [7]


def test_count_numbers_in_list(lst_of_numberss, empty_list, list_with_one_element) -> None:
    assert count_number_in_list(lst_of_numberss, 4) == 7
    assert count_number_in_list(lst_of_numberss, 1) == 2
    assert count_number_in_list(lst_of_numberss, 41) == 0
    assert count_number_in_list(empty_list, 4) == 0
    assert count_number_in_list(list_with_one_element, 4) == 0
    assert count_number_in_list(list_with_one_element, 7) == 1


@pytest.mark.parametrize(
    "shape, sides, expected",
    [
        ("square", [4], 16),
        ("rectangle", [4, 5], 20),
        ("triangle", [4, 5, 7], 9.797958971132712),
        ("circle", [3], 28.274333882308138),  # 3^2 * pi ≈ 28.27
        ("unknown", [1, 2, 3], None),
    ],
)
def test_calculate_area(shape, sides, expected):
    assert calculate_area(shape, sides) == pytest.approx(expected)  # Решение через pytest.approx()
    """# Этот инструмент сравнивает числа с определенным допуском (tolerance). 
    По умолчанию это 10^{-6}. «Если разница между числами ничтожна, считай, что они равны».
    """


@pytest.mark.parametrize(
    "coll, start, end, expected",
    [
        ("океанариум", 1, 4, "кеа"),
        ("океанариум", 0, None, "океанариум"),
        ("океанариум", 1, 3, "ке"),
        ("", 1, 3, []),  # пусто
        ("океанариум", 1, -1, "кеанариу"),
        ("океанариум", -6, -1, "нариу"),
        ("океанариум", 12, 30, ""),  # пусто
        ("океанариум", 3, None, "анариум"),
        ("океанариум", -1, 3, ""),  # пусто
    ],
)
def test_my_slice(coll, start, end, expected):
    assert my_slice(coll, start, end) == expected


@pytest.mark.parametrize(
    "dict1, dict2, expected",
    [
        ({"a": 1, "b": 2}, {"c": 3, "d": 4}, {"a": 1, "b": 2, "c": 3, "d": 4}),
        ({"a": 1, "b": 2}, {"b": 3, "c": 4}, {"a": 1, "b": 3, "c": 4}),
        ({}, {"c": 3, "d": 4}, {"c": 3, "d": 4}),
        ({"a": 1, "b": 2}, {}, {"a": 1, "b": 2}),
        ({}, {}, {}),
    ],
)
def test_merge_dicts(dict1, dict2, expected):
    assert merge_dicts(dict1, dict2) == expected


# Альтернативное решение
# Фикстуры для создания различных наборов словарей
@pytest.fixture
def dict1_no_overlap():
    return {"a": 1, "b": 2}


@pytest.fixture
def dict2_no_overlap():
    return {"c": 3, "d": 4}


@pytest.fixture
def dict1_with_overlap():
    return {"a": 1, "b": 2}


@pytest.fixture
def dict2_with_overlap():
    return {"b": 3, "c": 4}


@pytest.fixture
def empty_dict():
    return {}


# Параметризованные тесты
# # # Параметризованные тесты с ФИКСТУРАМИ, позволяет использовать с request & request.getfixturevalue
@pytest.mark.parametrize(
    "dict1_fixture, dict2_fixture, expected",
    [
        ("dict1_no_overlap", "dict2_no_overlap", {"a": 1, "b": 2, "c": 3, "d": 4}),
        ("dict1_with_overlap", "dict2_with_overlap", {"a": 1, "b": 3, "c": 4}),
        ("empty_dict", "dict2_no_overlap", {"c": 3, "d": 4}),
        ("dict1_no_overlap", "empty_dict", {"a": 1, "b": 2}),
        ("empty_dict", "empty_dict", {}),
    ],
)
def test_merge_dicts(dict1_fixture, dict2_fixture, expected, request):  # использовать с request
    dict1 = request.getfixturevalue(dict1_fixture)  # использовать request.getfixturevalue
    dict2 = request.getfixturevalue(dict2_fixture)
    assert merge_dicts(dict1, dict2) == expected


@pytest.mark.parametrize(
    "arr, target, expected",
    [
        ([1, 2, 3, 4, 5], 3, 2),  # Элемент в середине списка
        ([1, 2, 3, 4, 5], 1, 0),  # Первый элемент списка
        ([1, 2, 3, 4, 5], 5, 4),  # Последний элемент списка
        ([1, 2, 3, 4, 5], 6, -1),  # Элемент не найден
        ([10, 20, 30, 40, 50], 40, 3),  # Элемент в середине
        ([10, 20, 30, 40, 50], 25, -1),  # Элемент отсутствует
        ([], 3, -1),  # Пустой список
        ([1, 1, 1, 1, 1], 1, 2),  # Список с одинаковыми элементами
        ([-10, -5, 0, 5, 10], -5, 1),  # Список с отрицательными числами
        ([1], 1, 0),  # Список с одним элементом, элемент найден
        ([1], 2, -1),  # Список с одним элементом, элемент не найден
    ],
)
def test_binary_search(arr, target, expected):
    assert binary_search(arr, target) == expected


if __name__ == "__main__":
    pytest.main()  # запускает ВСЕ тесты из модуля
