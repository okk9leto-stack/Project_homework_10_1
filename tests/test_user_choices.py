import pytest
from pytest import MonkeyPatch

from src import user_choices

# Тесты get_user_choices_status()


def test_get_user_choices_status_valid_lowercase(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "executed")

    assert user_choices.get_user_choices_status() == "EXECUTED"


def test_get_user_choices_status_invalid_then_valid(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["UNKNOWN", "PENDING"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_choices_status() == "PENDING"


# Тесты get_user_choices_sortdays()


def test_get_user_choices_sortdays_descending(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["да", "по убыванию"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_choices_sortdays() is True


def test_get_user_choices_sortdays_ascending(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["да", "по возрастанию"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_choices_sortdays() is False


def test_get_user_choices_sortdays_no_sorting(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "нет")

    assert user_choices.get_user_choices_sortdays() is None


def test_get_user_choices_sortdays_invalid_answers(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["может быть", "да", "не знаю", "по убыванию"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_choices_sortdays() is True


# Тесты get_user_currency_choice()


def test_get_user_currency_choice_rub(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "да")

    assert user_choices.get_user_currency_choice() == "RUB"


def test_get_user_currency_choice_all(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "нет")

    assert user_choices.get_user_currency_choice() == "ALL"


def test_get_user_currency_choice_invalid_then_valid(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["не знаю", "да"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_currency_choice() == "RUB"


# Тесты get_user_choices_text()


def test_get_user_choices_text_search_enabled(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["да", "  ПЕРЕВОД  "])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_choices_text() == "перевод"


def test_get_user_choices_text_empty_then_nonempty(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["да", "   ", "покупка"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_choices_text() == "покупка"


def test_get_user_choices_text_search_disabled(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "нет")

    assert user_choices.get_user_choices_text() is None


def test_get_user_choices_text_invalid_answer(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["не знаю", "нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_choices_text() is None


# Тесты get_user_choices_type_file()


@pytest.mark.parametrize(
    ("answer", "expected_path"),
    [
        ("1", "data/operations.json"),
        ("2", "data/transactions_csv.csv"),
        ("3", "data/transactions_excel.xlsx"),
    ],
)
def test_get_user_choices_type_file_valid(monkeypatch: MonkeyPatch, answer: str, expected_path: str) -> None:
    monkeypatch.setattr("builtins.input", lambda _: answer)

    assert user_choices.get_user_choices_type_file() == expected_path


def test_get_user_choices_type_file_invalid_then_valid(monkeypatch: MonkeyPatch) -> None:
    answers = iter(["abc", "4", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert user_choices.get_user_choices_type_file() == "data/operations.json"


# Тесты get_user_choices_all()


def test_get_user_choices_all_returns_expected_dict(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        user_choices,
        "get_user_choices_type_file",
        lambda: "data/operations.json",
    )
    monkeypatch.setattr(
        user_choices,
        "get_user_choices_status",
        lambda: "EXECUTED",
    )
    monkeypatch.setattr(
        user_choices,
        "get_user_choices_sortdays",
        lambda: False,
    )
    monkeypatch.setattr(
        user_choices,
        "get_user_choices_text",
        lambda: "перевод",
    )
    monkeypatch.setattr(
        user_choices,
        "get_user_currency_choice",
        lambda: "RUB",
    )

    assert user_choices.get_user_choices_all() == {
        "file_path": "data/operations.json",
        "status": "EXECUTED",
        "sort_order": False,
        "text": "перевод",
        "currency": "RUB",
    }
