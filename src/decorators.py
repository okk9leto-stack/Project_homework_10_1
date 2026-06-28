import os
import time
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar

# Напишите декоратор log, который будет автоматически логировать начало и конец выполнения функции,
# а также ее результаты или возникшие ошибки.
# Декоратор должен принимать необязательный аргумент filename, который определяет,
# куда будут записываться логи (в файл или в консоль):
# Если filename задан, логи записываются в указанный файл. Если filename не задан, логи выводятся в консоль.
# Логирование должно включать:
# время вызова, имя функции, передаваемые аргументы, результат выполнения и информация об ошибках.
# Имя функции и результат выполнения при успешной операции.
# Имя функции, тип возникшей ошибки и входные параметры, если выполнение функции привело к ошибке.
# Пример использования декоратора:
# Ожидаемый вывод в лог-файл mylog.txt при успешном выполнении: # my_function ok
# Ожидаемый вывод при ошибке: # my_function error: тип ошибки. Inputs: (1, 2), {}
# Где тип ошибки заменяется на текст ошибки.
# Для правильной аннотации декоратора:
F = TypeVar("F", bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Декоратор log автоматически регистрирует детали выполнения функции и ее результат как в файл, так и в консоль.
    Декоратор принимает необязательный аргумент filename (имя файла, в который будут записываться логи).
    Если filename не задан, то логи выводятся в консоль.
    Если вызов функции закончился ошибкой, записывается сообщение об ошибке и входные параметры функции.
    """

    def wrapper(func: F) -> F:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            time_11 = time.ctime()
            try:
                time_1 = time.time()
                result = func(*args, **kwargs)
                time_2 = time.time()
                time_22 = time.ctime()
                message = (
                    f"Функция {func.__name__} Результат: ok\n Старт: {time_11}\n Стоп: {time_22}\n "
                    f"Время обработки: {time_2 - time_1: .6f}\n Аргументы {args}, {kwargs} \n "
                    f'Результат {result}\n {"-" * 50}  end \n'
                )
                if filename:
                    current_directory = os.path.dirname(__file__)
                    path_to_filename = str(os.path.join(current_directory, str(filename)))
                    with open(path_to_filename, "a", encoding="utf-8") as file:
                        file.write(message)
                else:
                    print(message)
                return result
            except Exception as e:
                error_type = type(e).__name__  # Получаем чистое название ошибки (например, TypeError)
                message = (
                    f"Функция {func.__name__}\n Результат: error {error_type} ({e})\n "
                    f'Старт: {time_11}\n Аргументы {args}, {kwargs} \n {"-" * 50} end \n'
                )
                if filename:
                    current_directory = os.path.dirname(__file__)
                    path_to_filename = str(os.path.join(current_directory, str(filename)))
                    with open(path_to_filename, "a", encoding="utf-8") as file:
                        file.write(message)
                else:
                    print(message)
                return e

        return inner  # type: ignore

    return wrapper


@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    return x + y


my_function(1, 4)

# Функция my_function Результат: ok
#  Старт: Sun Mar 29 09:37:37 2026
#  Стоп: Sun Mar 29 09:37:37 2026
#  Время обработки:  0.000001
#  Аргументы (1, 2), {}
#  Результат 3
#  --------------------------------------------------  end
# Функция my_function
#  Результат: error TypeError (unsupported operand type(s) for +: 'int' and 'str')
#  Старт: Sun Mar 29 09:38:51 2026
#  Аргументы (1, '2'), {}
#  -------------------------------------------------- end
#
# Используйте pytest для написания тестов, проверяющих функциональность декоратора.
# Для тестирования вывода в консоль примените фикстуру capsys
# , которая позволяет перехватывать вывод данных в консоль.
# Убедитесь, что тесты покрывают различные сценарии использования декоратора,
# включая успешное выполнение функций и обработку исключений.
