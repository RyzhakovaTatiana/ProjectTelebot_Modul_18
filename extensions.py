
import requests
import json
from config import keys

class APIException(Exception):
    pass

#Оформление исключений
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # Если пользователь переводит валюту в такую же валюту (рубль в рубль)
        if quote == base:
            raise APIException(f"Нельзя перевести одинаковые валюты {base}")
        #Если пользователь вводит невалидное название валюты
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Валюта {quote} мне не известна. Попробуй ввести валюту еще раз")
        # Если пользователь вводит невалидное название валюты
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Валюта {base} мне не известна. Попробуй ввести валюту еще раз")
        # Если пользователь вводит не целое число валюты
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        try:
            amount = float(amount)
        except TypeError:
            raise APIException(f"Не удалось обработать количество {amount}")


        quote_ticker, base_ticker = keys[quote], keys[base]
        # в первую переменную запишется первое значение, во вторую переменную второе, в третью переменную третье

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]
        #Будем возвращать произведение цены валюты на количество запрашиваемой валюты и округлим до сотых
        result = round(total_base * amount, ndigits= 2)
        return result