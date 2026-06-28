import math
import re


def sum_divisible_by_3_or_5(lst: list[int]) -> int:
    """
    Функция принимает на вход список чисел и возвращает сумму всех элементов списка,
    которые делятся на 3 или 5 без остатка.
    """
    result = 0
    for num in lst:
        if num % 3 == 0 or num % 5 == 0:
            result += num
    return result


def check_email(email: str) -> bool:
    i_1 = i_2 = 0
    for i, char in enumerate(email):
        if email[i] == "@":
            i_1 = i
        if email[i] == ".":
            i_2 = i
        else:
            continue
    if i_1 < i_2 and i_1 > 0 and i_2 - i_1 > 1 and email[-1] != ".":
        return True
    else:
        return False


def check_email_1(email):
    if not email:
        return False

    if "@" not in email or "." not in email:
        return False

    at_index = email.find("@")
    dot_index = email.find(".", at_index)

    # Проверяем, что '@' не первый символ, '.' не первый символ после '@', и '.' не последний символ
    if at_index < 1 or dot_index < at_index + 2 or dot_index == len(email) - 1:
        return False

    # Добавляем проверку на недопустимые символы в доменной части
    domain = email[at_index + 1 : dot_index]
    if not re.match(r"^[a-zA-Z0-9-]+$", domain):
        return False

    return True
    """
    re.match(): Эта функция проверяет, соответствует ли начало строки заданному регулярному выражению. 
    В данном случае, она проверяет, соответствует ли вся строка в переменной domain заданному шаблону.
    r"^[a-zA-Z0-9-]+$": Это само регулярное выражение:
    ^: Указывает на начало строки. Это означает, что проверка начнётся с самого начала строки.
    [a-zA-Z0-9-]: Это набор символов, который разрешён в доменной части email. Он включает:
    a-z: любые строчные буквы английского алфавита.
    A-Z: любые заглавные буквы английского алфавита.
    0-9: любые цифры.
    -: дефис (тире).
    +: Указывает, что один или более из перечисленных символов должны присутствовать. То есть, доменная часть должна содержать хотя бы один символ из указанного набора.
    $: Указывает на конец строки. Это значит, что после разрешённых символов больше ничего в строке быть не должно.
    """


# 1. В этом модуле - обычные данные, Фикстура - в test
def lst_of_numbers() -> list[int]:
    return [1, 2, 3, 1]


def count_number_in_list(lst_of_numbers, val_find) -> int:
    return list(lst_of_numbers).count(val_find)


def calculate_area(shape: str, sides: list[int | float]) -> float:
    """
    Функция принимает на вход название геометрической фигуры в виде строки
    и список ее сторон (в случае окружности список содержит радиус), а затем возвращает ее площадь.
    Функция поддерживает фигуры: квадрат, прямоугольник, треугольник, круг
    """
    if shape == "square":
        a = sides[0]
        return a**2
    elif shape == "rectangle":
        a, b = sides[0], sides[1]
        return a * b
    elif shape == "circle":
        a = sides[0]
        return math.pi * a**2
    elif shape == "triangle":
        a, b, c = sides[0], sides[1], sides[2]
        p = (a + b + c) / 2
        s = (p * (p - a) * (p - b) * (p - c)) ** 0.5
        return s
    else:
        return None


def my_slice(coll: str, start: int = 0, end: int = None) -> str | list:
    """
    Возвращает новый массив, содержащий копию части исходного массива.
    :coll: исходный список.
    :start: индекс, по которому начинается извлечение. Если индекс отрицательный,
    start указывает смещение от конца списка. По умолчанию равен нулю.
    :end: индекс, по которому заканчивается извлечение (не включая элемент с индексом end).
    Если индекс отрицательный, end указывает смещение от конца списка.
    По умолчанию равен длине исходного списка.
    :return: массив элементов
    """
    length = len(coll)
    if length == 0:
        return []

    normalized_end = length if end is None else end
    normalized_start = start

    if normalized_start < 0:
        if normalized_start < -length:
            normalized_start = 0
        else:
            normalized_start += length

    return coll[normalized_start:normalized_end]


def merge_dicts(dict1, dict2):
    merged = dict1.copy()  # Создаем копию первого словаря
    merged.update(dict2)  # Обновляем его значениями из второго словаря
    return merged


def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def binary_search_1(arr, target):
    try:
        return arr.index(target)
    except:
        return -1


if __name__ == "__main__":
    # print(sum_divisible_by_3_or_5([1,2,3]))
    # print(check_email('emai.l@mail.@rt'))# email@mail.ru
    # print(check_email_1('email@mail.'))
    # print(count_number_in_list(lst_of_numbers(),41))
    #
    # print(calculate_area('fd',[5]))
    # print(calculate_area('rectangle', [4, 5]))
    # print(calculate_area('triangle', [4, 5, 7]))
    # print(calculate_area('square', [4]))
    # print(calculate_area('circle', [5]))
    #
    # print(my_slice('океанариум', 0)) # океанариум
    # print (my_slice('океанариум',1,3)) # ке
    # print(my_slice('', 1, 3))  # ке
    # print(my_slice('океанариум', 1, -1)) # кеанариу
    # print(my_slice('океанариум', -6, -1)) # нариу
    # print(my_slice('океанариум', 12, 30)) # пусто
    # print(my_slice('океанариум', 3)) # анариум
    # print(my_slice('океанариум', -1, 3)) # пусто
    #
    print(binary_search([1, 2, 3, 4, 5], 5))
    print(binary_search_1([1, 2, 3, 4, 5], 5))
