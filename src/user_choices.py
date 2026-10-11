
def get_user_choices_status () -> str:
    """Собирает настройки обработки транзакций: возвращает выбранный СТАТУС операции."""

    status_list = ['EXECUTED', 'CANCELED', 'PENDING']

    print('Введите статус, по которому необходимо выполнить фильтрацию.')
    print(f'Доступные для фильтровки статусы: {', '.join(status_list)}')

    while True:
        choice_status = input('Выбери статус: ')  # Пользователь: "EXECUTED"
        status = choice_status.upper()

        if status in status_list:
            print(f'Операции отфильтрованы по статусу {status}')
            return status
            break

        print(f'Статус операции "{choice_status}" недоступен')  # Пользователь: "EEEEXECUTED"
        print('Введите статус, по которому необходимо выполнить фильтрацию.')
        print(f'Доступные для фильтрации статусы: {", ".join(status_list)}')


def get_user_choices_sortdays() -> str:
    """Собирает настройки обработки транзакций: возвращает необходимость СОРТИРОВКИ по дате и порядок сортировки."""
    while True:
        choices_sort_by_date = (input("Отсортировать операции по дате? Да/Нет: ")
                                .strip().lower())  # удалит пробелы из фактического ответа "Да/Нет" + переведет в нижний регистр

        if choices_sort_by_date in ['да', 'нет']:
            if choices_sort_by_date == "да":
                while True:
                    choices_sort_order = input("Сортировать по возрастанию или по убыванию? "
                                               ).strip().lower()
                    if choices_sort_order in ["по возрастанию", "по убыванию", ]:
                        print(f'Ваш выбор: "{choices_sort_by_date}",  сортировка "{choices_sort_order}"')
                        if choices_sort_order == "по убыванию":
                            return True
                        return False

                    print('Введите "по возрастанию" или "по убыванию"')

                return choices_sort_order

            choices_sort_order = None
            return choices_sort_order

        print('Выберите ответ "Да" или "Нет"')


def get_user_choices_currency () -> str:
    """Собирает настройки обработки транзакций: возвращает выбор валюты для фильтрации ("ALL"/"RUB")."""

    print('Выводить только рублевые транзакции? Да(только рублевые[RUB])/Нет(все валюты[ALL])')
    while True:
        choice_currency = ((input('Выводить только рублевые транзакции? Да/Нет: '))
                           .strip().lower())
        if choice_currency =='да':
            return 'RUB'
        elif choice_currency =='нет':
            return 'ALL'
        print('Выберите ответ "Да" или "Нет"')


def get_user_choices_text() -> str:
    """Собирает настройки обработки транзакций: возвращает необходимость поиска по тексту и текст для фильтрации."""
    while True:
        choices_text = (input("Фильтровать по слову в описании? Да/Нет: ")
                                .strip().lower())  # удалит пробелы из фактического ответа "Да/Нет" + переведет в нижний регистр

        if choices_text in ['да', 'нет']:
            if choices_text == "да":
                while True:
                    choices_text = input("Введите текст для поиска: _____ ").strip().lower()
                    if choices_text:
                        print(f'Фильтровать по : "{choices_text}"')
                        return choices_text
                    print('Текст для фильтра не выбран')
                    return None

            print('Поиск по тексту не требуется')
            return None

        print('Выберите ответ "Да" или "Нет"')


def get_user_choices_type_file() -> str:
    file_types = [
        {'number': 1, 'name': 'JSON', 'path': 'data/operations.json'},
        {'number': 2, 'name': 'CSV', 'path': 'data/transactions_csv.csv'},
        {'number': 3, 'name': 'XLSX', 'path': 'data/transactions_excel.xlsx'}
    ]

    print('Привет! Добро пожаловать в программу работы с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')

    for dict in file_types:
        print(f'{dict['number']}. Получить информацию о транзакциях из {dict['name']}-файла')
    numbers_types = [dict['number'] for dict in file_types]

    while True:
        try:
            choice_num = int(input(f'Выбери один из вариантов {numbers_types}: '))  # Пользователь: 1

            if choice_num in numbers_types:
                print(f'Для обработки выбран {file_types[choice_num - 1]['name']}-файл')
                return file_types[choice_num-1]['path']
            else:  # Пользователь: 4
                print(f'Выбери один из предложенных вариантов: {numbers_types}.')

        except ValueError:
            print(f'Нужно ввести число: {numbers_types}.')

if __name__ == '__main__':
    # print(get_user_choices_status())
    # print(get_user_choices_sortdays())
    # print(get_user_choices_currency())
    # print(get_user_choices_text())
    print(get_user_choices_type_file())

    # transactions_list = get_user_choices_transactions_list()
    # print(transactions_list)