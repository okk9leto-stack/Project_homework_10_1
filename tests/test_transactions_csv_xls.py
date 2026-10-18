from typing import Any
from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from src.transactions_csv_xls import read_file


# Тест для чтения CSV файла
@patch(
    "builtins.open",
    mock_open(
        read_data="id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;SOL;Alice;Bob;Перевод организации"
    ),
)
def test_read_csv_file() -> None:
    """
    Тест для CSV: проверяет, что функция read_file корректно считывает данные из CSV файла
    и возвращает их в виде списка словарей.
    Используются имитации (mock) для подмены функции open,
    чтобы симулировать чтение из файла без его фактического создания.
    """
    expected_result = [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "SOL",
            "from": "Alice",
            "to": "Bob",
            "description": "Перевод организации",
        }
    ]
    result = read_file("transactions_csv.csv")
    assert result == expected_result


# Тест для чтения Excel файла
@patch("pandas.read_excel")
def test_read_excel_file(mock_read_excel: Any) -> None:
    """
    Тест для Excel: проверяет, что функция read_file корректно обрабатывает Excel файлы.
    Для этого используется подмена (mock) функции pandas.read_excel,
    что позволяет симулировать чтение данных из Excel файла.
    """
    mock_data = pd.DataFrame(
        {
            "id": [650703],
            "state": ["EXECUTED"],
            "date": ["2023-09-05T11:30:32Z"],
            "amount": [16210],
            "currency_name": ["Sol"],
            "currency_code": ["SOL"],
            "from": ["Alice"],
            "to": ["Bob"],
            "description": ["Перевод организации"],
        }
    )
    mock_read_excel.return_value = mock_data

    expected_result = [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "SOL",
            "from": "Alice",
            "to": "Bob",
            "description": "Перевод организации",
        }
    ]
    result = read_file("transactions_excel.xlsx")
    assert result == expected_result


def test_read_file_valuerror() -> None:
    with pytest.raises(ValueError, match="Формат файла не поддерживается:"):
        read_file("transactions_cs.cs")


if __name__ == "__main__":
    test_read_csv_file()
    test_read_excel_file()
    test_read_file_valuerror()
    print("Все тесты прошли успешно!")
