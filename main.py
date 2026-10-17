from src.user_choices import get_user_choices_all
# from src.user_choices import get_user_choices_type_file
# from src.user_choices import get_user_choices_status
# from src.user_choices import get_user_choices_sortdays
# from src.user_choices import get_user_choices_text
# from src.user_choices import get_user_currency_choice
from src.search import process_bank_search
# from src.search import process_bank_operations
from src.search import filter_by_currency_json
from src.search import filter_by_currency_csv_xlsx
from src.transactions_csv_xls import read_file
from src.utils import operations_read
from src.processing import filter_by_state
from src.processing import sort_by_date

def main() -> list[dict]:
    """Основная функция программы обработки банковских транзакций."""

    # 1. Соберем все настройки пользователя.
    user_choices = get_user_choices_all()
    file_path = user_choices["file_path"]

    # 2. Читаем данные в зависимости от формата файла.
    if file_path.endswith((".csv", ".xlsx")):
        data = read_file(f"./{file_path}")

    elif file_path.endswith(".json"):
        data = operations_read(f"./{file_path}")

    else:
        raise ValueError(
            f'Формат файла не поддерживается: "{file_path}"'
        )

    # return data
    # 3.1 Применим фильтры из настроек: ключ status
    status = user_choices["status"]
    data = filter_by_state(data, status)


    # 3.2 Применим фильтры из настроек: строка поиска
    text = user_choices["text"] # ищет в "description": например "Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"
    if text is not None:
        data = process_bank_search(data, text)

    # 3.3 Применим фильтры из настроек: валюта
    currency = user_choices["currency"] # "ALL"/"RUB"

    if file_path.endswith((".csv", ".xlsx")):
        data = filter_by_currency_csv_xlsx(data, currency)

    elif file_path.endswith(".json"):
        data = filter_by_currency_json(data, currency)

    # 4. Отсортируем по дате
    sort_order = user_choices["sort_order"]
    if sort_order is not None:
        data = sort_by_date(data, sort_order)

    print(f'user_choices: {user_choices}')
    if data:
        print(f"Всего операций в выборке: {len(data)}")
        print("Список транзакций:")
        return data

    print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    return []



# def get_user_processing () -> str|list[dict]:
# ###### 1. Соберем все настройки обработки транзакций
#     # Собирает настройки обработки транзакций:
#     # Запрашивает тип файла и возвращает путь, по которому он расположен # file_types = {
#     #     1: {"name": "JSON", "path": "data/operations.json"},
#     #     2: {"name": "CSV", "path": "data/transactions_csv.csv"},
#     #     3: {"name": "XLSX", "path": "data/transactions_excel.xlsx"},}
#     get_user_choices_type_file()
#
#     # Собирает настройки обработки транзакций:
#     # возвращает выбранный СТАТУС операции "EXECUTED", "CANCELED", "PENDING"
#     get_user_choices_status()
#
#     # Собирает настройки обработки транзакций:
#     # возвращает необходимость СОРТИРОВКИ по дате и порядок сортировки:
#     # True — по убыванию, False — по возрастанию, None — сортировка не требуется
#     get_user_choices_sortdays()
#
#     # Собирает настройки обработки транзакций:
#     # Запрашивает необходимость поиска по тексту и возвращает текст для фильтра или None
#     get_user_choices_text()
#
#     # Собирает настройки обработки транзакций:
#     # Возвращает выбор валюты для фильтрации: 'RUB' или 'ALL'
#     get_user_currency_choice()
#
#     # Финально собирает все настройки обработки транзакций.: return {
#     #     # "file_path": get_user_choices_type_file(),
#     #     # "status": get_user_choices_status(),
#     #     # "sort_order": get_user_choices_sortdays(),
#     #     # "text": get_user_choices_text(),
#     #     # "currency": get_user_currency_choice()}
#     get_user_choices_all()
#
# ###### 2. С использованием пути из настроек используем соотв. файл и получим словарь с транзакциями
#     # transactions_csv_xls.read_file(file_path: str) -> List[Dict[Hashable, Any]]:
#     # Функция для считывания csv и xsl файлов.
#     read_file(file_path) # return data.to_dict(orient="records")
#
#     # utils.operations_read(path: Optional[str] = None) -> List[dict]:
#     # Функция принимает на вход путь до JSON-файла и возвращает список словарей
#     # с данными о финансовых транзакциях, в случае ошибки возвращает пустой список
#     operations_read(path = None) #return list(operations)
#
# ###### 3. Применим фильтры из настроек
#     # processing.filter_by_state(dict_state: List[Dict], state: str = "EXECUTED") -> List[Dict]:
#     # Функция принимает список словарей и значение для ключа (по умолчанию 'EXECUTED'),
#     # и возвращает новый список словарей, содержащий только те словари,
#     # у которых ключ state соответствует указанному значению
#     filter_by_state(dict_state, state)
#
#     # Возвращает операции, в описании которых есть строка поиска
#     process_bank_search(transactions_list, search_text)
#
#     # Функция принимает на вход список словарей с транзакциями и валюту,
#     # возвращает список словарей с транзакциями по выбранной валюте.
#     # Если валюта не выбрана, возвращает первоначальный список с транзакциями во всех валютах
#     filter_by_currency_json(transactions_list, currency = "ALL")
#
# ###### 4. Отсортируем
#     # processing/def sort_by_date(dict_state: List[Dict], sort_date: bool = True) -> List[Dict]:
#     # Функция, которая принимает список словарей и необязательный параметр,
#     # задающий порядок сортировки (по умолчанию — убывание).
#     # Функция должна возвращать новый список, отсортированный по дате (date)
#     sort_by_date(dict_state, sort_date = True)
#
# ###### 5. Еще посчитаем (необязательно, отдельная функция)
#     # Функция принимает список словарей с данными о банковских операциях и список категорий операций,
#     # и возвращает словарь, в котором ключи — это названия категорий,
#     # а значения — это количество операций в каждой категории
#     process_bank_operations(data, categories)

# ВЫВОД:
# Всего банковских операций в выборке: 4
# Список транзакций
# Если выборка оказалась пустой, программа выводит сообщение:
# print ('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации')

if __name__ == "__main__":
    print(main())
    # result = {'file_path': 'data/operations.json', 'status': 'EXECUTED', 'sort_order': None, 'text': None, 'currency': 'ALL'}
    # result = {'file_path': 'data/transactions_csv.csv', 'status': 'EXECUTED', 'sort_order': None, 'text': None, 'currency': 'ALL'}
    # result = {'file_path': 'data/transactions_excel.xlsx', 'status': 'EXECUTED', 'sort_order': None, 'text': None, 'currency': 'ALL'}
    # result = {'file_path': 'data/transactions_excel.xls', 'status': 'EXECUTED', 'sort_order': None, 'text': None, 'currency': 'ALL'}

    # data = operations_read('./data/operations.json') # для JSON-файлов
    # print(data[0])