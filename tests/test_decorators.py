import os
from typing import Any

from src.decorators import log


def test_log_positive_console(capsys: Any) -> None:
    """
    Тестирование ошибок для декоратора log
    Тест на успех: корректный ввод, функция возвращает правильный результат в консоль.
    """

    @log()
    def my_function(x: int, y: int) -> int:
        return x + y

    my_function(1, 2)
    result = capsys.readouterr()
    assert "Функция my_function Результат: ok\n" in result.out
    assert "Результат 3" in result.out


# Функция my_function Результат: ok
#  Старт: Sun Mar 29 09:37:37 2026
#  Стоп: Sun Mar 29 09:37:37 2026
#  Время обработки:  0.000001
#  Аргументы (1, 2), {}
#  Результат 3
#  -------------------------------------------------- end


def test_log_negative_console(capsys: Any) -> None:
    """
    Тестирование ошибок для декоратора log
    Тест на провал: при некорректных аргументах декоратор ловит TypeError, ValueError и другие ошибки, выводит в консоль
    """

    @log()
    def my_function(x: int, y: int) -> int:
        return x + y

    my_function(1, "2")  # type: ignore
    result = capsys.readouterr()
    assert "Функция my_function" in result.out
    assert "Результат: error TypeError" in result.out
    assert "unsupported operand type(s) for +: 'int' and 'str'" in result.out


# Функция my_function
#  Результат: error TypeError (unsupported operand type(s) for +: 'int' and 'str')
#  Старт: Sun Mar 29 10:16:58 2026
#  Аргументы (1, '2'), {}
#  -------------------------------------------------- end


def test_log_file_positive() -> None:
    """
        Тестирование ошибок для декоратора log
        Тест успех: корректный ввод, функция возвращает правильный результат в файл
    """
    # 1. Получаем путь к директории, в которой находится текущий файл
    current_directory = os.path.dirname(__file__)
    # 2. Формируем путь к файлу test_mylog.txt
    path_to_test_mylog = str(os.path.join(current_directory, "test_mylog.txt"))

    # 3. Оборачиваем функцию декоратором с этим путем
    @log(path_to_test_mylog)
    def my_function(x: int, y: int) -> int:
        return x + y

    # 4. Если в файле были записи - очистим для теста
    with open(path_to_test_mylog, "w", encoding="utf-8") as f:
        f.write(" ")

    # 5. Запускаем функцию
    my_function(10, 20)

    # 6. Проверяем, что файл создался
    assert os.path.exists(path_to_test_mylog)

    # 7. Читаем содержимое и проверяем через in
    with open(path_to_test_mylog, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Функция my_function" in content
        assert "Результат: ok" in content


def test_log_file_negative() -> None:
    """
        Тестирование ошибок для декоратора log
        Тест на провал: файл задан, при некорректных аргументах декоратор ловит TypeError, ValueError и другие ошибки и выводит в файл
        """
    # 1. Получаем путь к директории, в которой находится текущий файл
    current_directory = os.path.dirname(__file__)
    # 2. Формируем путь к файлу test_mylog.txt
    path_to_test_mylog = str(os.path.join(current_directory, "test_mylog.txt"))

    # 3. Оборачиваем функцию декоратором с этим путем
    @log(path_to_test_mylog)
    def my_function(x: int, y: int) -> int:
        return x + y

    # 4. Если в файле были записи - очистим для теста
    with open(path_to_test_mylog, "w", encoding="utf-8") as f:
        f.write(" ")

    # 5. Запускаем функцию
    my_function(10, "20")  # type: ignore

    # 6. Проверяем, что файл создался
    assert os.path.exists(path_to_test_mylog)

    # 7. Читаем содержимое и проверяем через in
    with open(path_to_test_mylog, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Функция my_function" in content
        assert "Результат: error TypeError" in content
