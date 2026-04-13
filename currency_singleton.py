"""
Модуль для работы с валютами ЦБ РФ
Реализован паттерн Singleton через метакласс
"""

import time
import requests
from xml.etree import ElementTree as ET
import matplotlib.pyplot as plt


class SingletonMeta(type):
    """
    Метакласс для реализации паттерна Singleton
    """
    _instance = None

    def __call__(cls, *args, **kwargs):
        # если объект еще не создан — создаем
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Currency:
    """
    Класс для хранения значения валюты
    (целая и дробная часть отдельно)
    """

    def __init__(self, name: str, value: str, nominal: int):
        self.name = name
        self.nominal = nominal

        # разделяем число на части
        integer, fractional = value.split(',')
        self.integer = integer
        self.fractional = fractional

    def get_value(self):
        """
        Возвращает значение в виде кортежа
        """
        return self.integer, self.fractional


class CurrencySingleton(metaclass=SingletonMeta):
    """
    Singleton класс для получения курсов валют
    """

    def __init__(self, delay: float = 1.0):
        self._delay = delay
        self._last_request_time = 0
        self._currencies = []

    def set_delay(self, delay: float):
        """Сеттер задержки"""
        self._delay = delay

    def get_delay(self):
        """Геттер задержки"""
        return self._delay

    def fetch_currencies(self, currencies_ids_lst: list) -> list:
        """
        Получение валют с сайта ЦБ
        """

        # защита от частых запросов
        current_time = time.time()
        if current_time - self._last_request_time < self._delay:
            print("Слишком частый запрос!")
            return []

        self._last_request_time = current_time

        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)

        result = []

        for valute in root.findall("Valute"):
            valute_id = valute.get('ID')

            if valute_id in currencies_ids_lst:
                name = valute.find('Name').text
                value = valute.find('Value').text
                char_code = valute.find('CharCode').text
                nominal = int(valute.find('Nominal').text)

                currency_obj = Currency(name, value, nominal)

                result.append({
                    char_code: (
                        currency_obj.name,
                        currency_obj.get_value()
                    )
                })

        # обработка неправильных id
        for cur_id in currencies_ids_lst:
            if cur_id not in [v.get('ID') for v in root.findall("Valute")]:
                result.append({cur_id: None})

        self._currencies = result
        return result

    def get_currencies(self):
        """Геттер списка валют"""
        return self._currencies

    def visualize_currencies(self):
        """
        Построение графика курсов валют
        """

        names = []
        values = []

        for item in self._currencies:
            for key, val in item.items():
                if val is None:
                    continue

                name, (integer, fractional) = val

                # собираем число обратно
                value = float(f"{integer}.{fractional}")

                names.append(key)
                values.append(value)

        plt.figure(figsize=(8, 5))
        plt.bar(names, values)

        plt.title("Курсы валют")
        plt.xlabel("Валюта")
        plt.ylabel("Курс")

        plt.savefig("currencies.jpg")
        plt.close()

    def __del__(self):
        """
        Деструктор
        """
        print("Объект CurrencySingleton удален")