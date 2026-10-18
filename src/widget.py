import src.masks


def mask_account_card(card_acc_number: str) -> str:
    """Функция принимает один аргумент — строку, содержащую тип и номер карты или счет и номер счета
    и возвращает строку с замаскированным номером"""

    # Примеры работы функции:
    # Visa Platinum 7000792289606361 --> Visa Platinum 7000 79** **** 6361 # для карты
    # Счет 73654108430135874305 --> Счет **4305 # для счета
    # Примеры входных данных: Maestro 1596837868705199 MasterCard 7158300734726758
    # Visa Classic 6831982476737658 Visa Platinum 8990922113665229 Visa Gold 5999414228426353
    # Счет 73654108430135874305 Счет 64686473678894779589 Счет 35383033474447895560

    if card_acc_number.replace(" ", "") == "":
        raise ValueError("Ошибка: введите реквизиты карты|счета")

    full_name = card_acc_number.split(" ")
    short_names = []
    only_num = ""

    for i, word in enumerate(full_name):
        if word.isalpha():
            short_names.append(word)
        if word.isdigit():
            only_num = word
    if len(only_num) != 16 and len(only_num) != 20:
        raise ValueError("Ошибка: некорректные реквизиты")
    if len(only_num) == 20:
        only_num = src.masks.get_mask_account(only_num)
    if len(only_num) == 16:
        only_num = src.masks.get_mask_card_number(only_num)
    return f'{" ".join(short_names)} {only_num}'


def get_date(date_in_full_format: str) -> str | None:
    """Функция, которая принимает на вход строку
    с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")"""
    date_in_full_format = date_in_full_format.replace(" ", "")

    if date_in_full_format == "":
        raise ValueError("Ошибка: Вы не ввели дату")

    if not all(date_in_full_format[i].isdigit() for i in [0, 1, 2, 3, 5, 6, 8, 9]):
        raise ValueError("Ошибка: формат даты некорректный")

    date_only = date_in_full_format[:10]  # == "2024-03-11"
    year, month, day = date_only.split("-")
    short_date = f"{day}.{month}.{year}"

    if int(day) > 31 or int(month) > 12:
        raise ValueError("Ошибка: формат даты некорректный")

    return short_date


# Вызов функциий # закомменчено, т.к. снижает % покрытия тестами
# if __name__ == "__main__":
#     result = mask_account_card(input("Введите реквизиты карты или счета:__"))
#     print(result)
#     fofmated_date = get_date(input("Введите дату в формате 2024-03-11T02:26:18.671407:__"))
#     print(fofmated_date)
