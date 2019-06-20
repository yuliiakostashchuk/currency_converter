"""Common helpers, used in both web API and CLI applications."""

import json

import requests
from currency import currency


def calculate_amount(amount, input_currency, output_currency):
    """
    Calculate the equivalent amount of foreign currency.
    :param float amount: Amount to convert
    :param str input_currency: ISO currency code
    :param str output_currency: ISO currency code
    :rtype: float
    :return: Equivalent amount
    """
    return amount * get_rate(input_currency, output_currency)


def get_rate(input_currency, output_currency):
    """
    Return specific exchange rate.
    :param str input_currency: ISO currency code
    :param str output_currency: ISO currency code
    :rtype: float
    :return: Rate
    """
    rates = get_rates(input_currency)  # Get all exchange rates against given currency

    return rates[output_currency]  # Return specific exchange rate


def get_rates(input_currency):
    """
    Return a dictionary of exchange rates against given currency available from https://exchangeratesapi.io.
    :param str input_currency: ISO currency code
    :rtype: dict
    :return: Dictionary of rates
    """
    base_url = "https://api.exchangeratesapi.io/latest?base="
    url = "".join([base_url, input_currency])

    r = requests.get(url)
    payload = r.json()

    return payload["rates"]


def set_symbols():
    """
    Return a dictionary of currency symbols available from external python library. (Symbol: ISO currency code).
    :param list curr: List of ISO currency codes
    :rtype: dict
    :return: Dictionary of currency symbols
    """
    curr = get_currencies()
    symbols = {}
    for item in curr:
        symbols[item] = currency.symbol(item)
    s = inv_dct(symbols)
    return s


def get_currencies():
    """
    Return a list of ISO currency codes.
    :rtype: list
    :return: List
    """
    curr = []
    for key in get_rates("EUR"):
        curr.append(key)
    curr.append("EUR")
    curr.sort()
    return curr


def inv_dct(dct):
    """
    Return an inverted dictionary. For example, from (ISO currency code: symbol) to (Symbol: ISO currency code).
    :param dict dct: Dictionary
    :rtype: dict
    :return: Inverted dictionary
    """
    d = {}
    for key, value in dct.items():
        if value in d.keys():
            d[value] = ", ".join([d[value], key])
        else:
            d[value] = key
    return d


def convert(amount, input_currency, output_currency="ALL"):
    """
    Currency converter
    :param float amount:
    :param str input_currency:
    :param str output_currency:
    :rtype: dict
    :return: Dictionary
    """

    all_symbols = set_symbols()

    if input_currency in all_symbols.keys():
        if ", " in all_symbols[input_currency]:
            return (
                "The input currency symbol is not unique. Please specify the ISO code."
            )
        else:
            input_currency = all_symbols[input_currency]

    if output_currency in all_symbols.keys():
        if ", " in all_symbols[output_currency]:
            return (
                "The output currency symbol is not unique. Please specify the ISO code."
            )
        else:
            output_currency = all_symbols[output_currency]

    results = {"input": {"amount": amount, "currency": input_currency}, "output": {}}

    if output_currency == "ALL":
        for currency in get_rates(input_currency):
            results["output"][currency] = calculate_amount(
                amount, input_currency, currency
            )
    else:
        results["output"][output_currency] = calculate_amount(
            amount, input_currency, output_currency
        )

    return results


def currencies_to_file():
    """
    Write a dictionary of currency symbols to a file currencies.txt
    :rtype: NoneType
    :return: None
    """
    with open("currencies.txt", "w+") as file:
        json.dump(set_symbols(), file, ensure_ascii=False, indent=2)
