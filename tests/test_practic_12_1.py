import pytest

from src.practic_12_1 import generate_users


@pytest.fixture
def data():
    return {
        "first_names": ["John", "Jane", "Mark", "Emily", "Michael", "Sarah"],
        "last_names": ["Doe", "Smith", "Johnson", "Brown", "Lee", "Wilson"],
        "cities": ["New York", "Los Angeles", "Chicago", "Houston", "Philadelphia"],
    }


def test_generate_users_num_users(data):
    """Проверяет, что количество сгенерированных пользователей равно запрошенному количеству пользователей."""
    num_users = 5
    users = [next(generate_users(**data)) for _ in range(num_users)]
    assert len(users) == num_users


def test_generate_users_keys(data):
    """Проверяет, что у всех сгенерированных пользователей есть правильные ключи."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert set(user.keys()) == {"first_name", "last_name", "age", "city"}


def test_generate_users_first_names(data):
    """Проверяет, что у всех сгенерированных пользователей имя является одним из возможных имен."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert user["first_name"] in data["first_names"]


def test_generate_users_last_names(data):
    """Проверяет, что у всех сгенерированных пользователей фамилия является одной из возможных фамилий."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert user["last_name"] in data["last_names"]


def test_generate_users_age(data):
    """Проверяет, что у всех сгенерированных пользователей возраст находится в заданном диапазоне."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert 18 <= user["age"] <= 65


def test_generate_users_cities(data):
    """Проверяет, что у всех сгенерированных пользователей город является одним из возможных городов."""
    users = [next(generate_users(**data)) for _ in range(5)]
    for user in users:
        assert user["city"] in data["cities"]


if __name__ == "__main__":
    #     pytest.main([__file__]) # проверить только текущий модуль
    pytest.main()  # запустить все тесты проекта разом (или все тесты в текущей директории)
