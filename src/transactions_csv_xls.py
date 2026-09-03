import os
from typing import Any
from typing import Dict
from typing import Hashable
from typing import List

import pandas as pd


def read_file(file_path: str) -> List[Dict[Hashable, Any]]:
    """Функция для считывания csv и xslx файлов.
    Функция принимает путь к файлу в формате строки и возвращает список словарей,
    где каждый словарь представляет одну запись из файла"""
    if file_path.endswith(".csv"):
        # Для CSV файлов используем read_csv с указанием разделителя
        data = pd.read_csv(file_path, sep=";")
    elif file_path.endswith(".xlsx"):
        # Для Excel файлов используем read_excel
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Формат файла не поддерживается: " + file_path)

    # Преобразуем DataFrame в список словарей
    return data.to_dict(orient="records")


# if __name__ == "__main__":
#     # Пример использования функции
#     base_dir = os.path.dirname(os.path.dirname(__file__))  # Поднимаемся на 2 уровня выше
#     path = os.path.join(base_dir, "data", "transactions_csv.csv")  # это для csv файла
#     # или
#     # path = os.path.join(base_dir, "data", "transactions_excel.xlsx")  # это для xlsx файла
#     csv_xls_data = read_file(path)
#     print(csv_xls_data)
