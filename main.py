import re


def clear_names(filename: str) -> list:
    """Функция для очистки имен от лишних символов"""
    clear_list = list()  # создадим пустой список для хранения очищенных имен
    with open(
        "../data/" + filename, encoding="utf-8"
    ) as user_file:  # поднялись уровнем выше до корневой директории ../ и сформировали путь к файлу
        new_name_list = user_file.read().split()
        for name_item in new_name_list:
            new_name = ""
            for symbol in name_item:
                if symbol.isalpha():
                    new_name += symbol
            if new_name.isalpha():
                clear_list.append(new_name)

    return clear_list


def is_cyrillic(name_item: str) -> bool:
    """Проверка на вхождение кириллицы в строку"""
    return bool(re.search("[а-яА-Я]", name_item))


def filter_russian_names(new_name_list: list) -> list:
    """Фильтрация имен написанных на русском"""
    clear_list = list()
    for name_item in new_name_list:
        if is_cyrillic(name_item):
            clear_list.append(name_item)
    return clear_list


def filter_english_names(new_name_list: list) -> list:
    """Фильтрация имен написанных на английском"""
    clear_list = list()
    for name_item in new_name_list:
        if not is_cyrillic(name_item):
            clear_list.append(name_item)
    return clear_list


def save_to_file(file_name: str, data: str) -> None:
    """Сохраняет данные в файл"""
    with open("../data/" + file_name, "w", encoding="utf-8") as user_file:
        user_file.write(data)


if __name__ == "__main__":
    cleared_name = clear_names("names.txt")

    filtered_names = filter_russian_names(cleared_name)
    save_to_file(file_name="russian_names.txt", data="\n".join(filtered_names))

    filtered_names = filter_english_names(cleared_name)
    save_to_file(file_name="english_names.txt", data="\n".join(filtered_names))
