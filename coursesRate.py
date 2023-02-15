import requests
from jsonsList import valuta

def rateToday(url):
    list_rate=[]
    data = requests.get(url).json()
    for v in valuta:
        list_rate.append((v, data['rates'][f'{v}']))
    return list_rate


def forRub(valueCtypt):
    valueCtypt

