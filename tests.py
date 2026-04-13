"""
Простые тесты для проверки работы
"""

from currency_singleton import CurrencySingleton


def test_invalid_id():
    singleton = CurrencySingleton()
    result = singleton.fetch_currencies(['R9999'])

    assert result[0] == {'R9999': None}


def test_valid_currency():
    singleton = CurrencySingleton()
    result = singleton.fetch_currencies(['R01035'])

    key = list(result[0].keys())[0]
    name, value = result[0][key]

    # проверяем название
    assert isinstance(name, str)

    # проверяем диапазон
    integer, fractional = value
    number = float(f"{integer}.{fractional}")

    assert 0 < number < 999


if __name__ == "__main__":
    test_invalid_id()
    test_valid_currency()
    print("Все тесты прошли!")