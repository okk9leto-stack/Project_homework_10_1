import json
import random
from typing import Dict
from typing import List

from more_itertools.recipes import quantify


def generate_users(first_names: list[str], last_names: list[str], cities: list[str]) -> dict:
    """Генерирует пользователя"""

    while True:
        user = {
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "age": random.randint(18, 65),
            "city": random.choice(cities),
        }
        yield user


def quantify_sum_transactions(func):
    """Декоратор для вывода статистики по отфильтрованным транзакциям."""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # Проверяем, есть ли данные, чтобы не упасть на result[0]
        if not result:
            print("Транзакции по выбранной валюте не найдены.")
            return result

        # def wrapper(*args, **kwargs): # смотри так красиииииво
        #     # 1. Достаем валюту из kwargs. Если вдруг в вызове её нет, используем 'Неизвестна' как заглушку
        #     currency = kwargs.get('currency', 'Неизвестна')
        #     result = func(*args, **kwargs)

        quantity = len(result)
        # currency = result[0]['currency'] # было так, далее заменим чтоб не вылетел при пустых
        currency = result[0].get("currency", "Не указана")
        # sum_amount = sum(x['amount'] for x in result) # было так, далее заменим чтоб не вылетел при пустых
        sum_amount = sum(x.get("amount", 0) for x in result)
        transactions_filtered_json = json.dumps(result, indent=4, ensure_ascii=False)
        print(
            f"Валюта: {currency}\n"
            f"Количество транзакций: {quantity}\n"
            f"Суммарная стоимость транзакций: {sum_amount}\n"
            f"Транзакции:\n{transactions_filtered_json}\n"
        )

        return result

    return wrapper


@quantify_sum_transactions
def filter_function_transactions(file_data: str, file_filtered: str, currency: str) -> list[dict]:
    """
    Напишите программу, которая будет принимать на вход JSON-файл с данными о финансовых транзакциях,
    фильтровать транзакции, совершенные в определенной валюте, и сохранять отфильтрованные данные в новый JSON-файл.
    Также напишите декоратор, который будет выводить в консоль статистику по количеству отфильтрованных транзакций.
    Статистика должна включать в себя количество отфильтрованных транзакций и их суммарную стоимость.
    """
    with open(file_data, "r", encoding="utf-8") as f:
        transactions = json.load(f)
        transactions_filtered = list(filter(lambda xx: xx.get("currency") == currency, transactions))
        # Или можно генератором: transactions_filtered = [xx for xx in transactions if xx.get('currency') == currency]
        # xx.get('currency') = xx['currency']
        # quantity = len(transactions_filtered)
        # sum_amount = sum(list(x ['amount'] for x in transactions_filtered))
        # transactions_filtered_json = json.dumps(transactions_filtered, indent=4, ensure_ascii=False)
        # print (f'Валюта: {currency}\nКоличество транзакций: {quantity}\nСуммарная стоимость транзакций: {sum_amount}\nТранзакции:\n{transactions_filtered_json}')
        with open(file_filtered, "w", encoding="utf-8") as ff:
            json.dump(transactions_filtered, ff, indent=4, ensure_ascii=False)
        return transactions_filtered


from datetime import datetime
from datetime import timedelta


def get_days_between_dates(date_start: str, date_end: str) -> int:
    """
        # Напишите функцию get_days_between_dates(date1, date2), которая принимает на вход две даты в формате "dd.mm.yyyy"
    # и возвращает количество дней между ними.
    """
    date_start_tm = datetime.strptime(date_start, "%d.%m.%Y")
    date_end_tm = datetime.strptime(date_end, "%d.%m.%Y")
    return (date_end_tm - date_start_tm).days


import requests


def get_github_repos(username: str) -> List[str]:
    """Получение списка репозиториев пользователя"""

    response = requests.get(f"https://api.github.com/users/{username}/repos")

    if response.status_code == 200:
        repos = [repo["full_name"] for repo in response.json()]
    else:
        repos = []
    return repos


# Написать функцию, которая будет принимать путь до файла и название города и выполнять следующие действия:
# Прочитать JSON-файл с данными о погоде в формате JSON.
# Выбрать из этого файла данные для города, который введет пользователь.
# Рассчитать среднюю температуру за неделю для выбранного города.
# Записать результат расчета в новый JSON-файл.
# Пример входного файла с данными (здесь запись в формате json):
# {
#   "Moscow": {
#     "Monday": 5,
#     "Tuesday": 2,
#     "Wednesday": -3,
#     "Thursday": -6,
#     "Friday": -2,
#     "Saturday": 0,
#     "Sunday": 2
#   },
#   "St. Petersburg": {
#     "Monday": 2,
#     "Tuesday": -1,
#     "Wednesday": -4,
#     "Thursday": -6,
#     "Friday": -1,
#     "Saturday": 1,
#     "Sunday": 3
#   },
#   "Kazan": {
#     "Monday": 1,
#     "Tuesday": -2,
#     "Wednesday": -6,
#     "Thursday": -7,
#     "Friday": -3,
#     "Saturday": 0,
#     "Sunday": 2
#   }}
#
# Пример выходного файла для города "Moscow":
# {"Moscow": {"Average temperature": -0.29}}

import json


def get_avg_for_city(path: str, city: str) -> bool:
    """Получение средней температуры за неделю для города"""
    try:
        with open(path) as city_file:
            try:
                city_data = json.load(city_file)
            except json.JSONDecodeError:
                print("Ошибка декодирования файла")
                return False
    except FileNotFoundError:
        print("Файл не найден")
        return False

    avg_temp = round(sum(city_data[city].values()) / len(city_data[city].keys()), 2)
    out_data = {city: {"Average temperature": avg_temp}}

    with open("practic_out.json", "w") as out_file:
        json.dump(out_data, out_file)

    return True


if __name__ == "__main__":
    get_avg_for_city("data.json", "Moscow")

# if __name__ == '__main__':
#     repos = get_github_repos('okk9leto-stack')
#     for repo in repos:
#         print(repo)

# if __name__ == '__main__':
# filter_function_transactions(file_data = 'practic_transactions.json', file_filtered='practic_transactions_filtered.json', currency = 'USD')

# if __name__ == '__main__':
# print(get_days_between_dates("01.01.2022", "31.01.2022"))  # 30

# cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia']
# first_names = ['John', 'Jane', 'Mark', 'Emily', 'Michael', 'Sarah']
# last_names = ['Doe', 'Smith', 'Johnson', 'Brown', 'Lee', 'Wilson']
#
# users = generate_users(first_names, last_names, cities)
#
# user_group1 = [next(users) for i in range(2)]
# user_group2 = [next(users) for i in range(1)]
#
# print('User group #1')
# print(json.dumps(user_group1, indent=4))
# print('User group #2')
# print(json.dumps(user_group2, indent=4))
# print('/////////////')
#
# num_users = 2
# users = [next(generate_users(first_names, last_names, cities)) for _ in range(num_users)]
# print (json.dumps(users, indent=2))
