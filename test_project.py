import pytest
from project import check_ticker, check_capital, get_data


def test_check_ticker():
    assert check_ticker("asdas") == False
    assert check_ticker("SDAX") == False
    assert check_ticker("SPY") == True


def test_check_capital():
    assert check_capital("asdasd") == False
    assert check_capital(0) == False
    assert check_capital(-5) == False
    assert check_capital(10000) == True


def test_get_data():
    with pytest.raises(Exception):
        get_data("asdasd", 10000)
