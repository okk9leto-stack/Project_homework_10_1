
def get_user_choices_status () -> str:
    """Собирает настройки обработки транзакций: возвращает выбранный СТАТУС операции."""

    status_list = ['EXECUTED', 'CANCELED', 'PENDING']

    print('Введите статус, по которому необходимо выполнить фильтрацию.')
    statuses = ', '.join(status_list)
    print(f'Доступные для фильтровки статусы: {statuses}')

    while True:
        choice_status = input('Выбери статус: ')  # Пользователь: "EXECUTED"
        status = choice_status.upper()

        if status in status_list:
            print(f'Операции отфильтрованы по статусу {status}')
            return status

        print(f'Статус операции "{choice_status}" недоступен')  # Пользователь: "EEEEXECUTED"
        print('Введите статус, по которому необходимо выполнить фильтрацию.')
        print(f'Доступные для фильтрации статусы: {", ".join(status_list)}')


def get_user_choices_sortdays() -> bool | None:
    """Собирает настройки обработки транзакций: возвращает необходимость СОРТИРОВКИ по дате и порядок сортировки:
    True — по убыванию,
    False — по возрастанию,
    None — сортировка не требуется."""

    while True:
        choices_sort_by_date = (input("Отсортировать операции по дате? Да/Нет: ")
                                .strip().lower())  # удалит пробелы из фактического ответа "Да/Нет" + переведет в нижний регистр

        if choices_sort_by_date == "да":
            while True:
                choices_sort_order = input("Сортировать по возрастанию или по убыванию? "
                                           ).strip().lower()
                if choices_sort_order in ["по возрастанию", "по убыванию", ]:
                    print(f'Ваш выбор: "{choices_sort_by_date}",  сортировка "{choices_sort_order}"')
                    if choices_sort_order == "по убыванию":
                        return True  # Сортировка по убыванию
                    return False  # Сортировка по возрастанию

                print('Введите "по возрастанию" или "по убыванию"')

        elif choices_sort_by_date == 'нет':
            print('Сортировка по дате не требуется.')
            return None

        else:
            print('Выберите ответ "Да" или "Нет"')


def get_user_currency_choice() -> str:
    """Собирает настройки обработки транзакций:
    Возвращает выбор валюты для фильтрации: 'RUB' или 'ALL'."""

    print(
        'Выводить только рублёвые транзакции?\n'
        'Да = только рубли (RUB).\n'
        'Нет = все валюты (ALL).'
    )

    while True:
        choice_currency = input('Ваш ответ (Да/Нет): ').strip().lower()

        if choice_currency == 'да':
            return 'RUB'

        elif choice_currency == 'нет':
            return 'ALL'

        print('Выберите ответ "Да" или "Нет".')


def get_user_choices_text() -> str|None:
    """Собирает настройки обработки транзакций:
    Запрашивает необходимость поиска по тексту
    и возвращает текст для фильтрации или None"""

    while True:
        survey_text = (input("Фильтровать по слову в описании? Да/Нет: ")
                                .strip().lower())  # удалит пробелы из фактического ответа "Да/Нет" + переведет в нижний регистр

        if survey_text == "да":
            while True:
                choices_text = input("Введите текст для поиска: _____ ").strip().lower()
                if choices_text:
                    print(f'Фильтровать по : "{choices_text}"')
                    return choices_text
                print('Текст для фильтра не выбран. Попробуйте снова.')
                # return None
        elif survey_text == "нет":
            print(f'Поиск по тексту не требуется')
            return None

        else:
            print('Выберите ответ "Да" или "Нет"')


def get_user_choices_type_file() -> str:
    """Собирает настройки обработки транзакций:
        Запрашивает тип файла и возвращает путь, по которому он расположен"""
    file_types = {
        1:{'name': 'JSON', 'path': 'data/operations.json'},
        2:{'name': 'CSV', 'path': 'data/transactions_csv.csv'},
        3:{'name': 'XLSX', 'path': 'data/transactions_excel.xlsx'}
    }

    print('Привет! Добро пожаловать в программу работы с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')

    for num, info in file_types.items():
        print(f'{num}. Получить информацию о транзакциях из {info["name"]}-файла')

    available_choices=list(file_types.keys())

    while True:
        try:
            choice_num = int(input(f'Выбери один из вариантов {available_choices}: ').strip())  # Пользователь: 1

            if choice_num in available_choices:
                file_info = file_types[choice_num]
                print(f"Для обработки выбран {file_info['name']}-файл")
                return file_info['path']

            print(f'Выбери один из предложенных вариантов: {available_choices}.') # Пользователь: 4

        except ValueError:
            print(f'Нужно ввести число: {available_choices}.')

def get_user_choices_all() -> dict:
    """Собирает все настройки обработки транзакций."""
    return {
        'file_path': get_user_choices_type_file(),
        'status': get_user_choices_status(),
        'sort_order': get_user_choices_sortdays(),
        'text': get_user_choices_text(),
        'currency': get_user_currency_choice()
    }

# if __name__ == '__main__':
    # print(get_user_choices_type_file())
    # print(get_user_choices_status())
    # print(get_user_choices_sortdays())
    # print(get_user_choices_text())
    # print(get_user_currency_choice())

    # print(get_user_choices_all())

    # transactions_list = get_user_choices_transactions_list()
    # print(transactions_list)