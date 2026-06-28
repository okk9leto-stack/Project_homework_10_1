l = [1, 2, 3, 4]

# def is_g (num):
#     return num >2
#
# print (list(filter(is_g,l)))

# Задача 1
# Напишите генератор, который принимает
# на вход последовательность чисел и генерирует квадраты этих чисел:


def square_generator(nums):
    for num in nums:
        yield num**2


# Способ 1: Сохранение в переменную (если нужно вызывать по одному)
print("--- Через переменную и next() ---")
my_gen = square_generator(l)  # Создали ОДИН объект
print(next(my_gen))  # Выведет 1
print(next(my_gen))  # Выведет 4
print(next(my_gen))  # Выведет 9

# Способ 2: Цикл for (самый правильный для всех элементов)
print("--- Через цикл for ---")
for square in square_generator(l):
    print(square)

# Задача 2
# генератор, который генерирует случайные числа в заданном диапазоне.
import random


def random_number_generator(start, stop):
    while True:
        yield random.randint(start, stop)


print("--- Случ. число через переменную и next() ---")
my_random = random_number_generator(1, 200)  # Создали ОДИН объект
print(next(my_random))  # Выведет число
print(next(my_random))  # Выведет другое число


# Задача 3
# Напишите генератор, который генерирует последовательность чисел по заданной формуле.


def func_generator(nums):
    for num in nums:
        yield num + 2.5


# Способ 1: Сохранение в переменную (если нужно вызывать по одному)
# l=[1,2,3,4]
print("--- func +2.5 через переменную и next() ---")
my_func = func_generator(l)  # Создали ОДИН объект
print(next(my_func))  # Выведет 3.5
print(next(my_func))  # Выведет 4.5
print(next(my_func))  # Выведет 5.5


# Еще Решение для Задачи 3
# Напишите генератор, который генерирует последовательность чисел по заданной формуле.
def formula(x):
    return x**2


def sequence_generator(start, formula):
    num = start
    while True:
        yield num
        num = formula(num)


print("--- formula через переменную и next() ---")
my_form = sequence_generator(2, formula)  # Создали ОДИН объект
print(next(my_form))  # Выведет 2
print(next(my_form))  # Выведет 4
print(next(my_form))  # Выведет 16


# Задача 4
# Напишите генератор, который принимает на вход два списка и генерирует элементы, которые есть в обоих списках.


def intersection_list(list_1, list_2):
    return set(list_1).intersection(set(list_2))


# вар-т -1
# def intersection_generator(list_1, list_2):
#     intersection_set = intersection_list (list_1, list_2)
#     for num in intersection_set:
#         yield num


# вар-т -2
def intersection_generator(list1, list2):
    seen = set()
    for item in list1:
        if item in list2 and item not in seen:
            seen.add(item)
            yield item


print("--- intersection_list через переменную и next() ---")
my_set = intersection_generator([2, 3, 4, 5], [3, 4, 5, 6, 7])  # Создали ОДИН объект
print(next(my_set))  # Выведет 3
print(next(my_set))  # Выведет 4
# print(next(my_set)) # Выведет 5


# print("--- test_intersection_list через переменную и next() ---")
# def test_intersection_generator ():
#     my_set_test = intersection_generator([7, 8, 9, 10], [8, 9, 10, 11, 12])  # Создали ОДИН объект
#     assert next(my_set_test) == 8
#     assert next(my_set_test) == 9
#     assert next(my_set_test) == 10

print("--- filter_orders_by_cost () ---")


def filter_orders_by_cost(f, cost):
    return list(filter(lambda x: x[2] >= int(cost), f))


f = [(1, 1, 10.0), (1, 2, 20.0), (2, 3, 15.0), (3, 4, 50.0), (3, 5, 30.0)]  # client_id, order_id, order_cost
result = filter_orders_by_cost(f, 20)

print(result)

print(" ")
print("--- 1_filter_orders_by_cost () with open lesson_11_orders.csv ---")


def filter_orders_by_cost(file_csv, cost):
    row_head = next(file_csv)  # client_id, order_id, order_cost

    rows = [row.split(",") for row in file_csv]

    clients = [int(row[0].rstrip()) for row in rows]
    orders = [int(row[1].rstrip()) for row in rows]
    all_orders_costs = [float(row[2].rstrip()) for row in rows]

    indexes = [i for i, x in enumerate(all_orders_costs)]
    indexes = list(filter(lambda x: all_orders_costs[x] >= cost, indexes))

    return [f"{clients[i]}, {orders[i]}, {all_orders_costs[i]}" for i in indexes]


with open("lesson_11_orders.csv", "r") as file:
    result = filter_orders_by_cost(file, 20)
print(result)


print(" ")
print("--- 2_filter_orders_by_cost () with open lesson_11_orders.csv ---")


def filter_orders_by_cost(file_csv, cost):
    row_head = next(file_csv)  # client_id, order_id, order_cost
    rows = [row.split(",") for row in file_csv]
    rows = [{"client_id": int(row[0]), "order_id": int(row[1]), "order_cost": float(row[2])} for row in rows]

    list_20 = list(filter(lambda row: row["order_cost"] >= cost, rows))

    #  return [index for index in list_20] - Вывод: [{'client_id': 1, 'order_id': 2, 'order_cost': 20.0}, {'client_id': 3, 'order_id': 4, 'order_cost': 50.0}, {'client_id': 3, 'order_id': 5, 'order_cost': 30.0}]
    return [
        f"{d['client_id']}, {d['order_id']}, {d['order_cost']}" for d in list_20
    ]  # Вывод: ['1, 2, 20.0', '3, 4, 50.0', '3, 5, 30.0']


with open("lesson_11_orders.csv", "r") as file:
    result = filter_orders_by_cost(file, 20)
print(result)


# Чтение чисел из файла и их обработка Дан текстовый файл nums.txt , содержащий список
print(" ")
print("--- Чтение чисел из файла и их обработка with open lesson_11_nums.txt ---")

import math  # чтобы потом применить math.isfinite(n) (бесконечность и "не число")


def clear_and_sum():
    with open("lesson_11_nums.txt") as file:
        rows = (row.split("#")[0].rstrip() for row in file)
        # row.split('#')[0] - в такой строке оставит только число "3 # inline comment"
        # .rstrip() удаляет пробелы, знаки табуляции, символы переноса строки (\n)
        nums = (float(n) for n in rows if n)
        nums = (n for n in nums if math.isfinite(n))
        # math.isfinite(n) (бесконечность и "не число")
        nums = (max(0.0, n) for n in nums)
        total_sum = sum(nums)
        return f"the sum is {total_sum}"


print(clear_and_sum())  # the sum is 15.0


print(" ")
print("---Генератор, который генерирует последовательность простых чисел----")


def primes():
    n = 2
    primes_list = []

    while True:
        if all(n % p != 0 for p in primes_list):
            yield n
        primes_list.append(n)
        n += 1


p = primes()
for i in range(7):
    print(next(p))


print(" ")
print("---Генератор чисел Фибоначчи----")


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


f = fibonacci()
for i in range(5):
    print(next(f))


print(" ")
print("---Тренажер 'Дурак' ----")


def joker(x_y=input("введите 2 числа от 0 до 6 через пробел: ")) -> str:
    x_y = list(map(int, x_y.split(" ")))
    x = x_y[0]
    y = x_y[1]
    if (x + y) > 8 or x > 6 or y > 6:
        raise ValueError("Ошибка: разберитесь с количеством козырей")
    elif x > y:
        joker_men = "Vova"
    elif x < y:
        joker_men = "Anton"
    else:
        joker_men = "Drow"
    return joker_men


# print (joker ())


print(" ")
print("---1_Тренажер 'наименьший натуральный делитель целого числа N, отличный от 1' ----")
# def smallest_div (a = int(input('введите число 1 < N ≤ 10^6: '))) -> int:
#     if a <=1 or a>10**6:
#         raise ValueError("Ошибка: введите число 1 < N ≤ 10^6")
#     for n in range(2, 10** 6):
#         if a % n == 0:
#             return n

# print(smallest_div ())


print(" ")
print("---2_Тренажер 'наименьший натуральный делитель целого числа N, отличный от 1' ----")

# import math
#
# def smallest_div(a = int(input('введите число 1 < N ≤ 10^6: '))) -> int:
#     if a <= 1 or a > 10**6:
#         raise ValueError("Ошибка: введите число 1 < N ≤ 10^6")
#     for n in range(2, int(math.sqrt(a)) + 1):
#         if a % n == 0:
#             return n
#     return a  # если не нашёл делитель, значит число простое

# print(smallest_div())
