import requests
import json
from token_cfg import currency


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_value = currency[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена! Перечень валют по команде /values")
        try:
            quote_value = currency[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена! Перечень валют по команде /values")

        if base_value == quote_value:
            raise APIException(f'Валюты совпадают {base}!')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        req = requests.get(f"https://api.exchangerate.host/convert?from={base_value}&to={quote_value}&amount={amount}")
        resp = json.loads(req.content)
        message = f"Цена {amount} {base_value} в {quote_value} : {round(resp['result'], 2)}"
        return message
