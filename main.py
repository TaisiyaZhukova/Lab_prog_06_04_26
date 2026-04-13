from currency_singleton import CurrencySingleton

if __name__ == "__main__":
    singleton = CurrencySingleton()

    result = singleton.fetch_currencies(
        ['R01035', 'R01335', 'R01700J']
    )

    print(result)

    singleton.visualize_currencies()
