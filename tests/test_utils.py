from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.utils import operations_read

# Тестирование
# Написаны тесты к новым функциональностям проекта.
# Тесты для функций конвертации валюты и открытия JSON-файла используют Mock и patch.
# Функциональный код покрыт тестами на 80% и больше.
# При запуске тестов командой pytest все тесты завершаются успешно.


def test_operations_read_not_path() -> None:
    assert (operations_read()) == []


def test_operations_read_FileNotFoundError() -> None:
    assert (operations_read("max.json")) == []


def test_operations_read_JSONDecodeError() -> None:
    assert (operations_read("./data/operations_error.json")) == []


def test_operations_read_not_list() -> None:
    assert (operations_read("./src/mylog.txt")) == []


@patch("src.utils.json.load")
def test_operations_read_not_list_mock(mock_json_load: MagicMock) -> None:
    """Тестируем случай, когда JSON содержит строку, используя Mock"""
    # 1. Задаем, что json.load вернет строку вместо ожидаемого списка
    mock_json_load.return_value = "это не список"

    # 2. Вызываем функцию. Путь может быть любым существующим,
    # так как данные в файл не попадут — их перехватит Mock.
    assert (operations_read("./data/operations.json")) == []

    # 3. Проверяем, что json.load действительно вызывался
    mock_json_load.assert_called_once()


def test_operations_read_is_dict() -> None:
    # файл успешно прочитается как словарь,
    # проверка isinstance(operations, list) даст False, тест для стр 31 utils.py
    assert operations_read("./data/not_a_list.json") == []


@patch("src.utils.json.load")
def test_operations_read_is_dict_mock(mock_json_load: MagicMock) -> None:
    """Тестируем случай, когда JSON содержит словарь вместо списка, используя Mock"""
    # 1. Задаем, что json.load вернет словарь вместо ожидаемого списка
    mock_json_load.return_value = {"key": "value"}

    # 2. Вызываем функцию. Путь может быть любым существующим,
    # так как данные в файл не попадут — их перехватит Mock.
    assert (operations_read("./data/operations.json")) == []

    # 3. Проверяем, что json.load действительно вызывался
    mock_json_load.assert_called_once()


def test_operations_read_ok() -> None:
    assert (operations_read("./data/operations.json")[0]) == {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }


if __name__ == "__main__":
    pytest.main()  # запускает ВСЕ тесты из модуля
