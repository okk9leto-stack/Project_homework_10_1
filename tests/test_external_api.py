from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import requests

from src.external_api import currency_conversion
from src.external_api import date_date
from src.external_api import get_api_key

# Тестирование
# Написаны тесты к новым функциональностям проекта.
# Тесты для функций конвертации валюты и открытия JSON-файла используют Mock и patch.
# Функциональный код покрыт тестами на 80% и больше.
# При запуске тестов командой pytest все тесты завершаются успешно.


def test_date_date_ok() -> None:
    assert (date_date("2019-04-19T12:02:30.129240")) == "2019-04-19"
    assert (date_date("2018-04-22T17:01:46.885252")) == "2018-04-22"


def test_date_date_valuerror() -> None:
    with pytest.raises(ValueError, match="корректный формат даты: "):
        date_date("2019-04-19 12:02:30")


@patch("src.external_api.os.getenv")  # mock_getenv
@patch("src.external_api.load_dotenv")  # mock_load
def test_get_api_have_key(mock_load: MagicMock, mock_getenv: MagicMock) -> None:
    # или так:
    # def test_get_api_key():
    #     with patch("src.external_api.load_dotenv") as mock_load:
    #         with patch("src.external_api.os.getenv") as mock_getenv:
    """Тест получения значения API_KEY из .env-файла с Mock (# Сценарий 1: Ключ есть)"""
    # 1. Задаем, что вернет Mock вместо переменных из .env-файла
    mock_getenv.return_value = "mysecretapikey"

    # 2. Вызываем функцию. данные из .env-файла не попадут — их перехватит Mock.
    assert (get_api_key()) == "mysecretapikey"

    # 3. Проверяем, что вызывался load_dotenv() # Загрузка переменных из .env-файла
    mock_load.assert_called_once()


@patch("src.external_api.os.getenv")
@patch("src.external_api.load_dotenv")
def test_get_api_key_none(mock_load: MagicMock, mock_getenv: MagicMock) -> None:
    """Тест получения значения API_KEY из .env-файла с Mock (# Сценарий 2: Ключа нет в .env)"""
    mock_getenv.return_value = None
    assert get_api_key() is None
    mock_load.assert_called_once()


@patch("src.external_api.get_api_key")  # mock_get_api_key
@patch("src.external_api.requests.get")  # mock_get
def test_currency_conversion_mock(mock_get: MagicMock, mock_get_api_key: MagicMock) -> None:
    """Позитивный сценарий: конвертация USD/EUR в RUB (тест успешного запроса к API с Mock)"""
    # 1. Настраиваем Mock для API-ключа
    mock_get_api_key.return_value = "test_api_key"
    # 2. Настраиваем заглушку для ответа сервера (requests.get)
    # Создаем объект, который будет имитировать response=requests.get(url..
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 75.0}}
    # Говорим, что при вызове requests.get вернется наш mock_response
    mock_get.return_value = mock_response
    # 3. Готовим входящие данные о транзакции
    transaction = {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2019-04-19T12:02:30.129240",
        "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
    }
    # 4. Вызываем функцию
    result = currency_conversion(transaction)
    # Добавляем проверку для Mypy, чтобы он понял, что это словарь, а не кортеж (были ошибки)
    assert isinstance(result, dict)
    # 5. Проверяем цифры: 100 USD * 75.0 курс = 7500.0 RUB
    assert result["RUB_amount"] == 7500.0
    assert result["rates"] == 75.0
    assert result["currency"] == "USD"

    # 6. Проверяем, что запрос ушел с правильным ключом в заголовках
    mock_get.assert_called_once()
    # Mock-объект записывает всё, что в него прилетело, в атрибут call_args,
    # какие данные функция пыталась отправить на сервер
    args, kwargs = mock_get.call_args
    assert kwargs["headers"] == {"apikey": "test_api_key"}


def test_currency_conversion_rub() -> None:
    """Валюта транзакции = RUB"""

    transaction = {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2019-04-19T12:02:30.129240",
        "operationAmount": {"amount": "100.00", "currency": {"name": "RUB", "code": "RUB"}},
    }
    result = currency_conversion(transaction)
    # Добавляем проверку для Mypy, чтобы он понял, что это словарь, а не кортеж (были ошибки)
    assert isinstance(result, dict)
    assert result["RUB_amount"] == 100.0
    assert result["currency"] == "RUB"
    assert result["rates"] == 1.0


@patch("src.external_api.get_api_key")  # mock_get_api_key
@patch("src.external_api.requests.get")  # mock_get
def test_currency_conversion_error_500(mock_get: MagicMock, mock_get_api_key: MagicMock) -> None:
    """Ошибка API: например, status_code 404 или 500"""
    # 1. Настраиваем API-ключ
    mock_get_api_key.return_value = "test_key"
    # 2. Создаем ответ сервера с ошибкой
    mock_response = MagicMock()
    mock_response.status_code = 500
    # заставляем метод raise_for_status выбросить ошибку
    # имитирует, когда интернет есть, но сервер ответил не так (не является корректным HTTP-ответом)
    # .side_effect -> мок делает действие (в нашем случае — «взрывается» ошибкой).
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Ошибка сервера")
    mock_get.return_value = mock_response
    # 3. Данные транзакции (USD, чтобы зайти в блок с запросом)
    transaction = {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2019-04-19T12:02:30.129240",
        "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
    }
    # 4. Вызываем функцию. Ожидаем, что блок except при ошибке API функция вернет {} (из стр. 65 прыгает в стр. 74)
    result = currency_conversion(transaction)
    # 5. Проверяем, что функция вернула пустой словарь
    assert result == {}


def test_currency_conversion_invalid_currency() -> None:
    """Неподдерживаемая валюта. Проверяем, что для валют остальных кроме USD, EUR возвращается пустой словарь"""
    transaction = {
        "date": "2023-10-01T12:02:30.129240",
        "operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}},  # Фунты не обрабатываются
    }

    result = currency_conversion(transaction)
    assert result == {}


@patch("src.external_api.get_api_key")
@patch("src.external_api.requests.get")
def test_currency_conversion_invalid_json(mock_get: MagicMock, mock_get_api_key: MagicMock) -> None:
    """Ошибка структуры JSON ответа (сервер ответил 200, но в JSON нет ключа 'rates' (KeyError))"""
    mock_get_api_key.return_value = "test_key"

    # Имитируем "неправильный" JSON от сервера
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": "Something went wrong"}  # Нет ключа 'rates'!

    mock_get.return_value = mock_response

    transaction = {
        "date": "2023-10-01T12:02:30.129240",
        "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}},
    }

    # Вызов функции приведет к KeyError на строке 68 с result["rates"]
    result = currency_conversion(transaction)

    # Благодаря блоку except, функция вернет {}
    assert result == {}


if __name__ == "__main__":
    pytest.main()  # запускает ВСЕ тесты из модуля
