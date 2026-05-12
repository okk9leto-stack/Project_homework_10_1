from typing import List
import json

# Обработка JSON-файла
# Файл с банковскими операциями размещен в директории data в корне проекта.
# Создан модуль utils  в пакете src.
# Реализована функция чтения JSON-файла в модуле utils.
# Функция чтения JSON-файла принимает путь к файлу JSON в качестве аргумента.
# Функция чтения JSON-файла возвращает список словарей с данными о финансовых транзакциях.
# Если JSON-файл пустой, содержит не-список или не найден, возвращается пустой список.


def operations_read (path:str)-> List[dict]:
    '''
    Функция принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях, в случае ошибки возвращает пустой список
    '''
    try:
        with open(path, 'r', encoding='utf-8') as operations_file:
            operations = json.load(operations_file)
    except (json.JSONDecodeError):
            print('Ошибка декодирования файла')
            operations = []
    except (FileNotFoundError):
            print('Файл не найден')
            operations = []
    return operations


if __name__ == '__main__':
    results = operations_read('../data/operations.json')
    for result in results:
        print(result)