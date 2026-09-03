import json
import logging
from typing import List
from typing import Optional

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


# Обработка JSON-файла
# Файл с банковскими операциями размещен в директории data в корне проекта.
# Создан модуль utils  в пакете src.
# Реализована функция чтения JSON-файла в модуле utils.
# Функция чтения JSON-файла принимает путь к файлу JSON в качестве аргумента.
# Функция чтения JSON-файла возвращает список словарей с данными о финансовых транзакциях.
# Если JSON-файл пустой, содержит не-список или не найден, возвращается пустой список.


def operations_read(path: Optional[str] = None) -> List[dict]:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях, в случае ошибки возвращает пустой список
    """

    if not path:  # путь к файлу не указан
        logger.info("Путь к файлу не указан")
        return []

    try:
        with open(path, "r", encoding="utf-8") as operations_file:
            operations = json.load(operations_file)  # ("../data/operations.json")

            # вернет True, если внутри лежит список, и False, если там что-то другое (строка, словарь, число, None)
            if isinstance(operations, list):
                logger.info("Создан список словарей")
                return list(operations)  # файл ок
            else:
                logger.info("Формат файла отличается от списка")
                return []  # "mylog.txt" формат не список

    # "max.json" нет такого файла & с ошибками "../data/operations_error.json"
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Произошла ошибка: {e}")
        return []


if __name__ == "__main__":
    results = operations_read("../data/operations.json")  # "../data/operations.json")
    print(results[0])
    # results[0] == {'id': 441945886, 'state': 'EXECUTED', 'date': '2019-08-26T10:50:58.294041',
    # 'operationAmount': {'amount': '31957.58', 'currency': {'name': 'руб.', 'code': 'RUB'}},
    # 'description': 'Перевод организации', 'from': 'Maestro 1596837868705199', 'to': 'Счет 64686473678894779589'}

for result in results:
    print(result)
