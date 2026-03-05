import pytest


@pytest.fixture
def card_number() -> str:  # для def get_mask_card_number(number: str) -> str: in masks
    return "7000792289606361"


@pytest.fixture()
def account_number() -> str:  # для def get_mask_account(number: str) -> str: in masks
    return "73654108430135874305"


@pytest.fixture()
def dict_state() -> list[dict]:
    # для def filter_by_state(dict_state: List[Dict], state: str = "EXECUTED") -> List[Dict]^ in processing.py
    # для def sort_by_date(dict_state: List[Dict], sort_date: bool = True) -> List[Dict]^  in processing.py
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture()
def date_full_format() -> str:  # для def get_date(date_in_full_format: str) -> str^ in widget.py
    return "2024-03-11T02:26:18.671407"
