from typing import List
import requests

from parsers.bank import Bank


class MonoBankParser(Bank):
    def __init__(self, currencies: List, bank_url: str, bank_id: int):
        # iso code as key used
        self.__currencies = {
            element[3]: (element[0], element[1]) for element in currencies
        }
        self.__bank_url = bank_url
        self.__bank_id = bank_id

    def __get_json(self):
        resp = requests.get(self.__bank_url)
        return resp.json()

    def get_currency_rate(self):
        currency_rate = {
            'bank_id': self.__bank_id,
            'rate': []
        }

        result = self.__get_json()
        for line in result:
            if str(line['currencyCodeA']) in self.__currencies.keys() and line['currencyCodeB'] == 980:
                currency_rate['rate'].append(
                     {
                         'currency_id': self.__currencies.get(str(line['currencyCodeA']))[0],
                         'purchase': round(float(line['rateBuy']), 2),
                         'sale': round(float(line['rateSell']), 2)
                     }
                )

        return currency_rate


if __name__ == '__main__':
    from connector import DbUtils
    from pprint import pprint

    db = DbUtils()
    db.connect()
    currencies = db.get_currencies()
    bank_id, bank_name, bank_url = db.get_bank_by_id(5)
    db.close()
    parser = MonoBankParser(currencies, bank_url, bank_id)
    pprint(parser.get_currency_rate())
