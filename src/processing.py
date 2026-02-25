from typing import Dict
from typing import List


def filter_by_state(dict_state: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция, которая принимает список словарей и опционально значение для ключа (по умолчанию 'EXECUTED'),
    и возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению
    """

    # Пример входных данных для проверки функции
    # [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    # {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    # {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    # {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    # Пример: выход функции со статусом по умолчанию 'EXECUTED'
    # [{'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    # {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    # Пример: выход функции, если вторым аргументом передано 'CANCELED'
    # [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    # {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

    new_dict_state = []
    for i, dict_i in enumerate(dict_state):
        if dict_i["state"] == state:
            new_dict_state.append(dict_i)
    return new_dict_state


def sort_by_date(dict_state: List[Dict], sort_date: bool = True) -> List[Dict]:
    """
    Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция должна возвращать новый список, отсортированный по дате (date)
    """
    # Пример входных данных для проверки функции
    # [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    # {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    # {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    # {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    # Пример: Выход функции (сортировка по убыванию, т. е. сначала самые последние операции)
    # [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    # {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    # {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    # {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

    dict_state_sort = sorted(dict_state, key=lambda dict_i: dict_i["date"], reverse=sort_date)
    return dict_state_sort


# Вызов функциий
if __name__ == "__main__":
    dict_state = [
        # Пример входных данных для проверки функции
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    result = filter_by_state(dict_state, "CANCELED")
    print(*result, sep="\n")
    # так список словарей печатает каждый словарь с новой строки, обязательно с *
    print("\n")

    result = sort_by_date(dict_state)
    print(*result, sep="\n")
    print("\n")

    result = sort_by_date(dict_state, False)
    print(*result, sep="\n")
